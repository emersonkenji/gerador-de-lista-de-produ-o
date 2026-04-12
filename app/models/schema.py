from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.connection import Base


class Store(Base):
    """Lojas/empresas extraídas automaticamente do XLSX."""
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ProductMapping(Base):
    """Mapeamento de produtos: título → tipo + litragem padrão."""
    __tablename__ = "products_mapping"

    id = Column(Integer, primary_key=True, index=True)
    title_pattern = Column(String, index=True, nullable=False)
    keywords = Column(String, nullable=True)
    product_type = Column(String, nullable=False)
    default_volume = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    variation_count = Column(Integer, default=0)
    auto_registered = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class TypeVariation(Base):
    """Variações customizadas de tipo de produto cadastradas pelo usuário."""
    __tablename__ = "type_variations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class VolumeVariation(Base):
    """Variações customizadas de litragem cadastradas pelo usuário."""
    __tablename__ = "volume_variations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ProductionList(Base):
    """Uma lista de produção gerada a partir de um XLSX importado."""
    __tablename__ = "production_lists"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String)
    list_date = Column(String)
    source_file_name = Column(String)
    source_file_datetime = Column(DateTime)
    raw_text_output = Column(Text)
    total_buckets = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    synced_at = Column(DateTime, nullable=True)
    sync_status = Column(String, default="pending")

    items = relationship("ProductionListItem", back_populates="production_list", cascade="all, delete-orphan")


class ProductionListItem(Base):
    """Um item individual dentro de uma lista de produção."""
    __tablename__ = "production_list_items"

    id = Column(Integer, primary_key=True, index=True)
    production_list_id = Column(Integer, ForeignKey("production_lists.id", ondelete="CASCADE"))
    product_type = Column(String)
    volume = Column(String)
    color = Column(String)
    quantity = Column(Integer, default=1)
    original_title = Column(String)
    original_variation = Column(String)
    store_name = Column(String, nullable=True)
    classification_status = Column(String, default="success")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    production_list = relationship("ProductionList", back_populates="items")


class AppSettings(Base):
    """Configurações gerais do aplicativo."""
    __tablename__ = "app_settings"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, default="E.F.S.T COMERCIAL LTDA")
    theme = Column(String, default="dark")
    supabase_url = Column(String, nullable=True)
    supabase_key = Column(String, nullable=True)
    enable_sync = Column(Boolean, default=False)
    github_repo = Column(String, default="")
    github_token = Column(String, default="")
    current_version = Column(String, default="1.0.0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
