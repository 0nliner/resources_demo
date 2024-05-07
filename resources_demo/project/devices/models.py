import typing
from typing import Optional
from datetime import datetime

from sqlalchemy import ForeignKey, String, case
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base, Denormalized, ImagesLinks, DocumentsLinks, DefautMetadata

if typing.TYPE_CHECKING:
    from resources.models import Node


# закоменченное - спорный код sh
# class Capability(Base):
#     __tablename__ = 'capability'
    
#     id: Mapped[int] = mapped_column(primary_key=True)
#     device_id: Mapped[int] = mapped_column(ForeignKey('device.id', ondelete='CASCADE'), nullable=False)
#     type: Mapped[str] = mapped_column(String(64), nullable=False)

#     # метаданные
#     min_value: Mapped[int] = mapped_column(nullable=True)
#     max_value: Mapped[int] = mapped_column(nullable=True)
#     address: Mapped[str] = mapped_column(String(128), nullable=True)
#     feedback_address: Mapped[str] = mapped_column(String(128), nullable=True)
#     unit: Mapped[str] = mapped_column(String(64), nullable=True)
#     # residence_id: Mapped[int] = mapped_column(ForeignKey('residence.id', ondelete='CASCADE'), nullable=True)
#     extra: Mapped[JSON] = mapped_column(JSONB, nullable=True)
#     updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
#     function: Mapped[str] = mapped_column(String(16), nullable=True)
#     push_enabled: Mapped[str] = mapped_column(String(16), nullable=True)
#     is_required: Mapped[bool] = mapped_column(Boolean, nullable=True)
#     sort_order: Mapped[int] = mapped_column(nullable=True)
#     is_hidden: Mapped[bool] = mapped_column(Boolean, nullable=True)


# class CapabilityTypes(Base):
#     __tablename__ = 'capability_types'
    
#     id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)
#     type: Mapped[str] = mapped_column(String(64), nullable=False)
#     device_type_id: Mapped[int] = mapped_column(ForeignKey('device_types.id', ondelete='CASCADE'), nullable=True)

#     is_required: Mapped[bool] = mapped_column(Boolean, nullable=False)
#     function: Mapped[str] = mapped_column(String(16), nullable=True)
#     updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
#     is_hidden: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
#     displayed_name: Mapped[str] = mapped_column(String(64), nullable=True)
#     displayed_function_name: Mapped[str] = mapped_column(String(64), nullable=True)
#     value_units: Mapped[JSON] = mapped_column(JSONB, nullable=True)
#     # access_modifier: Mapped[str] = mapped_column(String(16), nullable=True)


# class Controller(Base):
#     __tablename__ = 'controller'
    
#     id: Mapped[int] = mapped_column(primary_key=True)
#     # метаданные
#     serial_number: Mapped[str] = mapped_column(String(32), nullable=True)
#     uid: Mapped[str] = mapped_column(String(128), nullable=False)
#     ip: Mapped[str] = mapped_column(String(32), nullable=True)
#     port: Mapped[int] = mapped_column(nullable=False)
#     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
#     updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
#     extra: Mapped[JSONB] = mapped_column(nullable=True)
#     is_registered: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
#     is_dhcp: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
#     # apartment_id: Mapped[int] = mapped_column(ForeignKey('apartment.id', ondelete='CASCADE'), nullable=True)
#     # residence_id: Mapped[int] = mapped_column(ForeignKey('residence.id', ondelete='CASCADE'), nullable=True)

# (Base)


class Property(DefautMetadata, ImagesLinks, DocumentsLinks, Denormalized):
    """
    объект имущества
    """
    __tablename__ = 'properties'

    id: Mapped[int] = mapped_column(primary_key=True)
    node_id: Mapped[int] = mapped_column(ForeignKey('nodes.id'))
    type: Mapped[str] = mapped_column(String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'properties',
        'polymorphic_on': case(
                (type == "device", "device"),
                (type == "controller", "controller"),
                else_="properties")}

    # TODO: вернуть
    node: Mapped['Node'] = relationship('Node', back_populates="properties")


class Manufacturer(DefautMetadata, Denormalized):
    __tablename__ = "manufacturers"

    id: Mapped[int] = mapped_column(primary_key=True)


class DeviceType(DefautMetadata, Denormalized):
    __tablename__ = 'device_types'
    
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)


class DeviceModel(DefautMetadata, ImagesLinks, Denormalized):
    __tablename__ = "device_models"

    id: Mapped[int] = mapped_column(primary_key=True)
    type_id: Mapped[int] = mapped_column(ForeignKey('device_types.id', ondelete='CASCADE'), nullable=True)
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey('manufacturers.id', ondelete='CASCADE'), nullable=True)
    
    manufacturer: Mapped[Manufacturer] = relationship(Manufacturer)
    type: Mapped[DeviceType] = relationship(DeviceType)
    devices: Mapped["Device"] = relationship("Device", back_populates="device_model")


class Device(Property):
    __mapper_args__ = {'polymorphic_identity': 'device'}
    
    device_model_id: Mapped[int] = mapped_column(ForeignKey('device_models.id', ondelete='CASCADE'))
    device_model: Mapped[DeviceModel] = relationship(DeviceModel)

    # метаданные
    icon_tag: Mapped[str] = mapped_column(String(512), nullable=True)
    

    # driver_id: Mapped[int] = mapped_column(ForeignKey('drivers.id', ondelete='CASCADE'), nullable=True)
    # warnings: Mapped[JSONB] = mapped_column(nullable=True)
    # has_commands: Mapped[bool] = mapped_column(Boolean, nullable=True)
    # has_feedbacks: Mapped[bool] = mapped_column(Boolean, nullable=True)
    # is_complete: Mapped[bool] = mapped_column(Boolean, nullable=True)

    # TODO: добавить ссылку на node
    # room_id: Mapped[int] = mapped_column(ForeignKey('room.id', ondelete='CASCADE'), nullable=True)
    # residence_id: Mapped[int] = mapped_column(ForeignKey('residence.id', ondelete='CASCADE'), nullable=True)
    # subtype: Mapped[str] = mapped_column(String(128), nullable=False)

    
class Controller(Device):
    __mapper_args__ = {'polymorphic_identity': 'controller'}
    
