from typing import Optional, Union, TYPE_CHECKING
from enum import Enum
# скорее всего будет отдельным сервисом
from sqlalchemy import JSON, ARRAY, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core import Base

if TYPE_CHECKING:
    from users.models import User


STR_ARR = ARRAY(String(100))


class PolicyCheckStatuses(Enum):
    ALLOWED = "ALLOWED"
    DENIED = "DENIED"
    ALLOWED_NO_OTHER_CONDITIONS = "ALLOWED_NO_OTHER_CONDITIONS"


class All(type):
    ...


class Policy(Base):
    __tablename__ = "polices"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    policy_on: Mapped[str] # на какой ресурс устанавливаем политику ?
    action: Mapped[str]
    # special_users: Mapped[list[int]]
    # allowed_for_spaces: Mapped[Union[list[int]]]
    # awailable_fields_to_interact: Mapped[list[str]]
    # disabled_fields_to_interact: Mapped[list[str]]
    # response_hidden_fields: Mapped[list[str]]
    policy: Mapped[dict] = mapped_column(JSON, nullable=True)
    conditions: Mapped[list[str]] = mapped_column(STR_ARR)
