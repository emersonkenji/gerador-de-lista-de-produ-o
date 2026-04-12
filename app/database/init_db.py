from .connection import engine, Base, SessionLocal
from app.models.schema import (
    AppSettings, ProductMapping, ProductionList, ProductionListItem,
    Store, TypeVariation, VolumeVariation
)


# Tipos e volumes padrão
DEFAULT_TYPES = ["Econômica", "Piso", "Externa", "Emborrachada", "Premium"]
DEFAULT_VOLUMES = ["3,6L", "10L", "18L", "500ml"]


def init_db():
    """Cria todas as tabelas e insere dados padrão se necessário."""
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Settings padrão
        settings = db.query(AppSettings).first()
        if not settings:
            settings = AppSettings(
                company_name="E.F.S.T COMERCIAL LTDA",
                theme="dark",
                current_version="1.0.0"
            )
            db.add(settings)
            db.commit()

        # Tipos padrão
        for t in DEFAULT_TYPES:
            exists = db.query(TypeVariation).filter(TypeVariation.name == t).first()
            if not exists:
                db.add(TypeVariation(name=t))
        db.commit()

        # Volumes padrão
        for v in DEFAULT_VOLUMES:
            exists = db.query(VolumeVariation).filter(VolumeVariation.name == v).first()
            if not exists:
                db.add(VolumeVariation(name=v))
        db.commit()

    finally:
        db.close()
