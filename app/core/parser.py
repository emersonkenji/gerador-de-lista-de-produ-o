import re
import unicodedata


def normalize_text(text: str) -> str:
    """Remove acentos, converte para minúsculas e limpa espaços duplicados."""
    if not text or not isinstance(text, str):
        return ""
    text = text.lower().strip()
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'\s+', ' ', text)
    return text


def extract_volume(text: str) -> str | None:
    """Extrai a litragem de um texto (variação ou título)."""
    text_norm = normalize_text(text)

    # Prioriza volumes mencionados com vírgula (como em variação "Cor,10L")
    if re.search(r',\s*3[.,]\s*6\s*(l|litros?)\b', text_norm):
        return "3,6L"
    if re.search(r',\s*10\s*(l|litros?)\b', text_norm):
        return "10L"
    if re.search(r',\s*18\s*(l|litros?)\b', text_norm):
        return "18L"
    if re.search(r',\s*500\s*ml\b', text_norm):
        return "500ml"

    # Depois procura padrões em "literosN" ou "NL" (compactos como "18l" ou "18 litros")
    if re.search(r'\b18\s*(?:l|litro)s?\b', text_norm):
        return "18L"
    if re.search(r'\b10\s*(?:l|litro)s?\b', text_norm):
        return "10L"
    if re.search(r'\b3[.,]\s*6\s*(?:l|litro)s?\b', text_norm):
        return "3,6L"
    if re.search(r'\b500\s*ml\b', text_norm):
        return "500ml"

    return None


def count_volumes_in_text(text: str) -> int:
    """Conta quantos tamanhos diferentes aparecem em um texto."""
    text_norm = normalize_text(text)
    count = 0
    
    if re.search(r'\b18\s*(?:l|litro)s?\b', text_norm):
        count += 1
    if re.search(r'\b10\s*(?:l|litro)s?\b', text_norm):
        count += 1
    if re.search(r'\b3[.,]\s*6\s*(?:l|litro)s?\b', text_norm):
        count += 1
    if re.search(r'\b500\s*ml\b', text_norm):
        count += 1
    
    return count


def determine_type_from_text(text: str) -> str | None:
    """Identifica o tipo de tinta a partir do título."""
    text_norm = normalize_text(text)

    type_patterns = [
        (r'\b(emborrachad[ao]|emborrachara|emborracghara)\b', "Emborrachada"),
        (r'\b(piso)\b', "Piso"),
        (r'\b(extern[ao])\b', "Externa"),
        (r'\b(intern[ao]|interiores|parede|economic[ao])\b', "Econômica"),
        (r'\b(premium)\b', "Premium"),
    ]

    for pattern, type_name in type_patterns:
        if re.search(pattern, text_norm):
            return type_name

    return None


def extract_color(variation_text: str, volume_str: str | None = None) -> str:
    """Extrai a cor da variação removendo volume se presente."""
    if not variation_text or variation_text.lower() == "nan":
        return "Indefinida"

    text = variation_text

    # Remove volume patterns
    text = re.sub(r',?\s*3[.,]\s*6\s*(l|litros?)\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r',?\s*10\s*(l|litros?)\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r',?\s*18\s*(l|litros?)\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r',?\s*500\s*(ml)\s*', '', text, flags=re.IGNORECASE)

    # Clean leftover commas and spaces
    text = text.strip().strip(',').strip()

    if text:
        return text.strip().title()
    return "Indefinida"


def parse_product(title: str, variation: str) -> dict:
    """Analisa título e variação para extrair tipo, volume e cor."""
    # Volume: prioridade variação > título
    volume = extract_volume(variation)
    if not volume:
        volume = extract_volume(title)

    color = extract_color(variation, volume)

    # Se a variação só tem a cor sem vírgula
    if color == "Indefinida" and variation and variation.lower() != "nan":
        cleaned = variation.strip()
        if cleaned:
            color = cleaned.title()

    product_type = determine_type_from_text(title)

    return {
        "volume": volume,
        "color": color,
        "product_type": product_type
    }
