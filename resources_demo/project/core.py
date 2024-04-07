from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
from users.datamappers import SSOUserDM


Base = declarative_base()


class CallerDTO(SSOUserDM, BaseModel):
    ...
