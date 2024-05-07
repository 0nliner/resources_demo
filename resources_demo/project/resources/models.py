from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, String, case
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core import ImagesLinks, DefautMetadata, DocumentsLinks, Denormalized

if TYPE_CHECKING:
    from devices.models import Property


class Node(ImagesLinks, DefautMetadata, DocumentsLinks, Denormalized):
    __tablename__ = 'nodes'

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey('nodes.id'), nullable=True, default=None)
    parent: Mapped['Node'] = relationship("Node", back_populates="children", remote_side=[id])
    children: Mapped[Optional[list['Node']]] = relationship('Node', back_populates="parent")
    type: Mapped[str] = mapped_column(String(50), default="nodes")
    properties: Mapped[list['Property']] = relationship('Property', back_populates="node")

    __mapper_args__ = {
        'polymorphic_identity': 'nodes',
        "polymorphic_on": type,
        # 'polymorphic_on': case(
        #         (type == "floor", "floor"),
        #         (type == "rooms", "rooms"),
        #         (type == "buildings", "buildings"),
        #         (type == "building_complexes", "building_complexes"),
        #         else_="nodes")
    }


class Floor(Node):
    # __tablename__ = 'floors'
    __mapper_args__ = {'polymorphic_identity': 'floor'}
    # id: Mapped[int] = mapped_column(ForeignKey('nodes.id'), primary_key=True)
    level: Mapped[Optional[int]]


class Room(Floor):
    # __tablename__ = 'rooms'
    __mapper_args__ = {'polymorphic_identity': 'rooms'}
    # id: Mapped[int] = mapped_column(ForeignKey('floors.id'), primary_key=True)
    room_number: Mapped[Optional[str]]


class Building(Node):
    # __tablename__ = 'buildings'
    __mapper_args__ = {'polymorphic_identity': 'buildings'}
    # id: Mapped[int] = mapped_column(ForeignKey('nodes.id'), primary_key=True)
    address: Mapped[Optional[str]]


class BuildingComplex(Node):
    # __tablename__ = 'building_complexes'
    __mapper_args__ = {'polymorphic_identity': 'building_complexes'}
    # id: Mapped[int] = mapped_column(ForeignKey('nodes.id'), primary_key=True)
    complex_name: Mapped[Optional[str]]
