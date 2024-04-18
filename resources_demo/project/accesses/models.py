# скорее всего будет отдельным сервисом
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column
from core import Base


class Policy(Base):
    __table_name__ = "polices"
    
    id: Mapped[int]
    policy_on: Mapped[str]
    policy: Mapped[JSON] = mapped_column(nullable=True)
