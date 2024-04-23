from typing import Optional
import typing
from sqlalchemy import ARRAY, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from pydantic import BaseModel, ConfigDict
from users.datamappers import SSOUserDM
from enum import auto, Enum

from lib import Blank, DTOField, DTOBase


Base = declarative_base()


class CallerDTO(SSOUserDM, BaseModel):
    role_id: int


class ReportFormats(Enum):
    pdf = auto()
    word = auto()


class ReportBy(Enum):
    period = auto()


class BidSubjects(Enum):
    test_subjects = auto()

# 
class EditableMetadata(DTOBase):
    name: DTOField[str] = Blank
    description: DTOField[str] = Blank
    extra: DTOField[str] = Blank
    comments: DTOField[str] = Blank


class EditableMetadataDM(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    extra: Optional[str] = None
    comments: Optional[str] = None


class ActionOnEditableMetadataMixin(DTOBase):
    name: DTOField[str] = Blank
    description: DTOField[str] = Blank
    extra: DTOField[str] = Blank
    comments: DTOField[str] = Blank

# 
class ImagesLinks(Base):
    __abstract__ = True
    images: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String(100)), nullable=True)


class DocumentsLinks(Base):
    __abstract__ = True
    docs: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String(100)), nullable=True)


from sqlalchemy import DateTime
from datetime import datetime

class Dates(Base):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)


# Base, 
class DefautMetadata(Dates):
    __abstract__ = True
    name: Mapped[Optional[str]] = mapped_column(String(128))
    description: Mapped[Optional[str]] = mapped_column(String(1024))
    # extra: Mapped[JSONB] = mapped_column(nullable=True)
    comments: Mapped[Optional[str]] = mapped_column(nullable=True)
