from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

from core import EditableMetadataDM
from lib.interfaces import DMBase


class NodesDM(DMBase):
    ...


class NodeDM(EditableMetadataDM, DMBase):
    id: int
    parent_id: Optional[int] = None


class ImageDM(DMBase):
    id: str

    @property
    def url(self) -> str:
        ...
