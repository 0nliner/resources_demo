from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class NodesDM(BaseModel):
    ...


class NodeDM(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    parent_id: Optional[int]


class ImageDM(BaseModel):
    id: str

    @property
    def url(self) -> str:
        ...
