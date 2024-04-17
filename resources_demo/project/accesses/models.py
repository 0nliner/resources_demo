from sqlalchemy.orm import Mapped, mapped_column
from core import Base


class Accesss(Base):
    __table_name__ = "accesses"
    
    id: mapped_column[int]
    node: int


