import pandas as pd
import openpyxl  # Forçando inclusão pelo PyInstaller
from datetime import datetime
from collections import defaultdict
import re
import logging

from app.core.parser import parse_product, normalize_text, extract_volume
from app.models.schema import ProductMapping, Store

logger = logging.getLogger(__name__)


def extract_date_from_filename(filename: str) -> tuple[str, datetime]:
    """Extrai data e datetime do nome do arquivo Export_Order..."""
    match = re.search(r'(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})', filename)
    if match:
        year, month, day, h, m, s = match.groups()
        dt = datetime(int(year), int(month), int(day), int(h), int(m), int(s))
        return f"{day}/{month}/{year}", dt
    return datetime.now().strftime("%d/%m/%Y"), datetime.now()


def auto_register_stores(df: pd.DataFrame, db_session) -> list[str]:
    """Cadastra automaticamente as lojas que aparecem no XLSX."""
    col = "Nome da Loja no UpSeller"
    if col not in df.columns:
        return []

    store_names = df[col].dropna().unique().tolist()
    registered = []

    for name in store_names:
        name = str(name).strip()
        if not name:
            continue
        existing = db_session.query(Store).filter(Store.name == name).first()
        if not existing:
            db_session.add(Store(name=name))
            registered.append(name)

    if registered:
        db_session.commit()
        logger.info(f"Lojas registradas automaticamente: {registered}")

    return registered


def auto_register_products(df: pd.DataFrame, db_session) -> list[str]:
    """Cadastra automaticamente os produtos novos a partir dos títulos do XLSX.
    Títulos idênticos = mesmo produto com variações diferentes.
    """
    col_title = "Nome do Anúncio"
    col_variation = "Variação"

    if col_title not in df.columns:
        return []

    # Agrupa variações por título
    title_variations: dict[str, set] = defaultdict(set)
    for _, row in df.iterrows():
        title = str(row.get(col_title, "")).strip()
        variation = str(row.get(col_variation, "")).strip()
        if title and title != "nan":
            if variation and variation != "nan":
                title_variations[title].add(variation)
            else:
                title_variations[title].add("(sem variação)")

    registered = []
    for title, variations in title_variations.items():
        norm_title = normalize_text(title)

        # Verifica se já existe um mapeamento que cubra esse título
        existing_mappings = db_session.query(ProductMapping).filter(
            ProductMapping.is_active == True
        ).all()

        already_mapped = False
        for m in existing_mappings:
            pattern = normalize_text(m.title_pattern)
            keys = [normalize_text(k) for k in (m.keywords or "").split(",") if k.strip()]
            if pattern and (pattern in norm_title or norm_title in pattern):
                already_mapped = True
                # Atualiza contagem de variações
                m.variation_count = max(m.variation_count or 0, len(variations))
                break
            if any(k and k in norm_title for k in keys):
                already_mapped = True
                m.variation_count = max(m.variation_count or 0, len(variations))
                break

        if not already_mapped:
            # Tenta inferir tipo e volume do título
            from app.core.parser import determine_type_from_text, extract_volume
            inferred_type = determine_type_from_text(title) or "Outros"
            inferred_volume = extract_volume(title)

            new_map = ProductMapping(
                title_pattern=title,
                keywords="",
                product_type=inferred_type,
                default_volume=inferred_volume,
                is_active=True,
                auto_registered=True,
                variation_count=len(variations)
            )
            db_session.add(new_map)
            registered.append(title[:60])

    if registered:
        db_session.commit()
        logger.info(f"Produtos registrados automaticamente: {len(registered)}")

    return registered


def process_dataframe(df: pd.DataFrame, db_session) -> list[dict]:
    """Processa o DataFrame e retorna lista de registros classificados."""
    records = []

    # Auto-registrar lojas e produtos
    auto_register_stores(df, db_session)
    auto_register_products(df, db_session)

    # Recarregar mapeamentos após auto-registro
    mappings = db_session.query(ProductMapping).filter(ProductMapping.is_active == True).all()

    for _, row in df.iterrows():
        title = str(row.get("Nome do Anúncio", ""))
        variation = str(row.get("Variação", ""))
        store = str(row.get("Nome da Loja no UpSeller", ""))

        try:
            quantity = int(row.get("Qtd. do Produto", 1))
        except (ValueError, TypeError):
            quantity = 1

        parsed = parse_product(title, variation)

        # Cruzar com mapeamento do banco
        mapped_type = None
        mapped_volume = None
        normalized_title = normalize_text(title)

        for m in mappings:
            keys = [normalize_text(k) for k in (m.keywords or "").split(",") if k.strip()]
            pattern = normalize_text(m.title_pattern)

            if pattern and (pattern in normalized_title or normalized_title in pattern):
                mapped_type = m.product_type
                if m.default_volume:
                    mapped_volume = m.default_volume
                break

            if any(k and k in normalized_title for k in keys):
                mapped_type = m.product_type
                if m.default_volume:
                    mapped_volume = m.default_volume
                break

        variation_vol = extract_volume(variation)

        final_type = mapped_type or parsed['product_type']
        final_volume = variation_vol or mapped_volume or parsed['volume']

        status = "success"
        if not final_type:
            status = "pending"
            final_type = "Outros"  # Será resolvido pelo popup de classificação
        if not final_volume:
            status = "pending"
            final_volume = "Indefinida"

        records.append({
            "product_type": final_type,
            "volume": final_volume,
            "color": parsed['color'],
            "quantity": quantity,
            "original_title": title,
            "original_variation": variation,
            "store_name": store,
            "classification_status": status
        })

    return records


def generate_text_output(grouped_data: dict, company_name: str, date_str: str) -> tuple[str, int]:
    """Gera a saída textual formatada da lista de produção."""
    lines = []
    lines.append(f"🎨 LISTA DE PRODUÇÃO - {company_name}")
    lines.append(f"📅 Data: {date_str}")
    lines.append("=" * 60)
    lines.append("")

    total_buckets = 0

    type_order = {"Econômica": 1, "Piso": 2, "Externa": 3, "Emborrachada": 4, "Premium": 5, "Outros": 99}
    vol_order = {"3,6L": 1, "10L": 2, "18L": 3, "500ml": 4, "Indefinida": 99}

    sorted_types = sorted(grouped_data.keys(), key=lambda t: type_order.get(t, 98))

    for pt in sorted_types:
        lines.append(f"{pt.upper()}:")
        vols = grouped_data[pt]
        sorted_vols = sorted(vols.keys(), key=lambda v: vol_order.get(v, 98))

        for vol in sorted_vols:
            lines.append(f"  Tinta {pt.lower()} {vol}:")
            colors = vols[vol]
            for c in sorted(colors.keys()):
                q = colors[c]
                lines.append(f"    {c.lower()} - {q}")
                total_buckets += q
        lines.append("")

    lines.append("📊 RESUMO GERAL:")
    lines.append(f"Total de baldes produzidos: {total_buckets}")

    return "\n".join(lines), total_buckets
