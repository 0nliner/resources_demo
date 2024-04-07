from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core import Base


class Node(Base):
    __tablename__ = 'nodes'

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey('nodes.id'), nullable=True, default=None)
    parent: Mapped['Node'] = relationship("Node", back_populates="children", remote_side=[id])
    children: Mapped[Optional[list['Node']]] = relationship('Node', back_populates="parent")


class Floor(Node):
    __tablename__ = 'floors'

    id: Mapped[int] = mapped_column(ForeignKey('nodes.id'), primary_key=True)
    level: Mapped[int]


class Room(Floor):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(ForeignKey('floors.id'), primary_key=True)
    room_number: Mapped[str]


class Building(Node):
    __tablename__ = 'buildings'

    id: Mapped[int] = mapped_column(ForeignKey('nodes.id'), primary_key=True)
    address: Mapped[str]


class BuildingComplex(Node):
    __tablename__ = 'building_complexes'

    id: Mapped[int] = mapped_column(ForeignKey('nodes.id'), primary_key=True)
    complex_name: Mapped[str]
