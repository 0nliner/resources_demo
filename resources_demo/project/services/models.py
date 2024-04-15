import uuid
from sqlalchemy import ForeignKey, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core import Base


class ServiceCategory(Base):
    __tablename__ = 'service_category'
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, type_=String(36))
    title: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    icon_tag: Mapped[str] = mapped_column(String(32), nullable=True)
    service_pattern_layout_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('service_layout_pattern.id'), type_=String(36), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=True)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # service_pattern_layout = relationship("ServiceLayoutPattern", back_populates="service_category")

    def __str__(self):
        return str(self.id)


class Service(Base):
    __tablename__ = 'service'
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, type_=String(36))
    service_category: Mapped[ServiceCategory] = relationship("ServiceCategory", back_populates="service")

    # метаданные
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    short_description: Mapped[str] = mapped_column(String(64), nullable=True)
    long_description: Mapped[str] = mapped_column(Text, nullable=True)
    publication_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    service_category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('service_category.id'), type_=String(36), nullable=True)
    provider_company_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('provider_company.id'), type_=String(36), nullable=True)
    image_url: Mapped[str] = mapped_column(String(1024), nullable=True)
    image_thumbnail_url: Mapped[str] = mapped_column(String(1024), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    # хз
    # reporting: Mapped[str] = mapped_column(String(64), nullable=True)  # Choices handling in SQLAlchemy differs from Django
    # grid_width: Mapped[int] = mapped_column(Integer, nullable=True)  # Choices handling in SQLAlchemy differs from Django

    is_internal: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=True)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # provider_company: Mapped[] = relationship("ProviderCompany", back_populates="service")
    # Many-to-many relationships require association tables in SQLAlchemy
    
    def __str__(self):
        return str(self.id)
