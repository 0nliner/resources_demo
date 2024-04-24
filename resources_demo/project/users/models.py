from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from core import Base


class User(Base):
    __tablename__ = 'users'
    
    # указывает на id пользователя в keycloak
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False, autoincrement=False)
    extra: Mapped[dict] = mapped_column(JSON, nullable=True)
    # image_id: Mapped[int] = mapped_column(
    #           ForeignKey('image.id', ondelete='CASCADE'),
    #           nullable=True)

    # language: Mapped[SupportedLanguages] = mapped_column(
    #           Enum(SupportedLanguages),
    #           nullable=False,
    #           server_default=str(SupportedLanguages.get_default()))
