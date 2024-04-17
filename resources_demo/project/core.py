from typing import Optional
from sqlalchemy import ARRAY, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from pydantic import BaseModel
from users.datamappers import SSOUserDM
from enum import auto, Enum



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


class EditableMetadata(BaseModel):
    name: Optional[str]
    description: Optional[str]
    extra: Optional[str]
    comments: Optional[str]


class ImagesLinks(Base):
    __abstract__ = True
    images: Mapped[list[str]] = mapped_column(ARRAY(String(100)))


class DocumentsLinks(Base):
    __abstract__ = True
    docs: Mapped[list[str]] = mapped_column(ARRAY(String(100)))


from sqlalchemy import DateTime
from datetime import datetime

class Dates(Base):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)


# Base, 
class DefautMetadata(Dates):
    __abstract__ = True
    name: Mapped[Optional[str]] = mapped_column(String(128), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(1024))
    # extra: Mapped[JSONB] = mapped_column(nullable=True)
    comments: Mapped[Optional[str]] = mapped_column(nullable=True)
