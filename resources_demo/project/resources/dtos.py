from typing import Optional
from pydantic import BaseModel, ConfigDict
from core import CallerDTO


class CreateNodeDTO(BaseModel):
    parent_id: Optional[int] = None


class DeleteNodeDTO(BaseModel):
    ...


class UpdateNodeDTO(BaseModel):
    ...

class RetrieveNodeDTO(BaseModel):
    id: int


# множества
class CreateNodesDTO(BaseModel):
    ...


class DeleteNodesDTO(BaseModel):
    ...


class UpdateNodesDTO(BaseModel):
    ...


class ListNodesDTO(BaseModel):
    caller: CallerDTO
