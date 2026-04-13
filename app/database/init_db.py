import sqlite3
from .connection import engine, Base, SessionLocal, DB_PATH
from app.models.schema import (
    AppSettings, ProductMapping, ProductionList, ProductionListItem,
    Store, TypeVariation, VolumeVariation
)
from app.version import VERSION


DEFAULT_TYPES = ["Econômica", "Piso", "Externa", "Emborrachada", "Premium"]
DEFAULT_VOLUMES = ["3,6L", "10L", "18L", "500ml"]


def _migrate_db():
    """Adiciona colunas que faltam em tabelas existentes (migração simples)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Migrações: (tabela, coluna, tipo, default)
    migrations = [
        ("app_settings", "github_token", "TEXT", "''"),
        ("app_settings", "github_repo", "TEXT", "''"),
        ("app_settings", "current_version", "TEXT", f"'{VERSION}'"),
        ("products_mapping", "auto_registered", "INTEGER", "0"),
        ("products_mapping", "variation_count", "INTEGER", "0"),
        ("production_list_items", "store_name", "TEXT", "''"),
    ]

    for table, col, col_type, default in migrations:
        try:
            cursor.execute(f"SELECT {col} FROM {table} LIMIT 1")
        except sqlite3.OperationalError:
            try:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col} {col_type} DEFAULT {default}")
            except Exception:
                pass

    conn.commit()
    conn.close()


def init_db():
    """Cria todas as tabelas, roda migrações e insere dados padrão."""
    Base.metadata.create_all(bind=engine)
    _migrate_db()

    db = SessionLocal()
    try:
        settings = db.query(AppSettings).first()
        if not settings:
            settings = AppSettings(
                company_name="Colorvil",
                theme="dark",
                current_version=VERSION
            )
            db.add(settings)
            db.commit()

        for t in DEFAULT_TYPES:
            if not db.query(TypeVariation).filter(TypeVariation.name == t).first():
                db.add(TypeVariation(name=t))
        db.commit()

        for v in DEFAULT_VOLUMES:
            if not db.query(VolumeVariation).filter(VolumeVariation.name == v).first():
                db.add(VolumeVariation(name=v))
        db.commit()

    finally:
        db.close()
