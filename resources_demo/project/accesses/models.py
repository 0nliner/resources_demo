# скорее всего будет отдельным сервисом
from sqlalchemy import JSON, ARRAY, String
from sqlalchemy.orm import Mapped, mapped_column
from core import Base


class Policy(Base):
    __tablename__ = "polices"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    policy_on: Mapped[str]
    policy: Mapped[dict] = mapped_column(JSON, nullable=True)
    conditions: Mapped[list[str]] = mapped_column(ARRAY(String(100)))
