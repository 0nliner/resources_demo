from typing import Optional
from enum import auto, Enum
from datetime import datetime

from sqlalchemy import ARRAY, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

from pydantic import BaseModel
from lib import (Blank, DTOField, DTOBase, BaseSelection, Expressions)

from users.datamappers import SSOUserDM



Base = declarative_base()

# базовые объекты и структуры
class CallerDTO(SSOUserDM, BaseModel):
    role_id: int


class ReportFormats(Enum):
    pdf = auto()
    word = auto()


class ReportBy(Enum):
    period = auto()


class BidSubjects(Enum):
    test_subjects = auto()


# базовые датамапперы
class EditableMetadataDM(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    extra: Optional[str] = None
    comments: Optional[str] = None


# базовые dto
class EditableMetadata(DTOBase):
    name: DTOField[str] = Blank
    description: DTOField[str] = Blank
    extra: DTOField[str] = Blank
    comments: DTOField[str] = Blank


# базовые селекшены
class IdSelection(BaseSelection):
    id: Expressions[int] = Blank

class DateSelection(BaseSelection):
    created_at: Expressions[datetime] = Blank
    updated_at: Expressions[datetime] = Blank

class DefaultMetadataSelection(BaseSelection):
    name: Expressions[str] = Blank
    description: Expressions[str] = Blank
    comments: Expressions[str] = Blank

# TODO: сделать проверку на то, что хотя бы одно поле заполнено в конечном селекшене

#  абстрактные модели алхимии
from sqlalchemy import DateTime


class ImagesLinks(Base):
    __abstract__ = True
    images: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String(100)), nullable=True)


class DocumentsLinks(Base):
    __abstract__ = True
    docs: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String(100)), nullable=True)


class Dates(Base):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)


class DefautMetadata(Dates):
    __abstract__ = True
    name: Mapped[Optional[str]] = mapped_column(String(128))
    description: Mapped[Optional[str]] = mapped_column(String(1024))
    # extra: Mapped[JSONB] = mapped_column(nullable=True)
    comments: Mapped[Optional[str]] = mapped_column(nullable=True)
