from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID

from lib import DTOBase

# class CreateServiceCategoryDTO(DTOBase):
#     id
#     title


class CreateServiceDTO(DTOBase):
    title: str
    short_description: str
    long_description: str
    service_category: UUID
    is_active: bool
    is_internal: bool
    image_url: Optional[str]
    image_thumbnail_url: Optional[str]
    # под замену
    provider_company: UUID
    residences: list[UUID]
    employees: list[UUID]
    # нло
    # reporting: "no_report"
    # sort_order: int
    # grid_width: int
    # realty_object_types: list[UUID]
    

class RetieveServiceDTO(DTOBase):
    id: int


class UpdateServicePayload(BaseModel):
    title: Optional[str]
    short_description: Optional[str]
    long_description: Optional[str]
    service_category: Optional[UUID]
    is_active: Optional[bool]
    is_internal: Optional[bool]
    image_url: Optional[str]
    image_thumbnail_url: Optional[str]


class UpdateServiceDTO(DTOBase):
    id: int
    payload: UpdateServicePayload


class DeleteServiceDTO(DTOBase):
    id: int


#  категории
class CreateServiceCategoryDTO(DTOBase):
    title: str
    is_active: Optional[bool]
    icon_tag: Optional[str]


class RetrieveServiceCategoryDTO(DTOBase):
    id: int


class UpdateServiceCategoryPayload(BaseModel):
    title: Optional[str]
    is_active: Optional[bool]
    icon_tag: Optional[str]


class UpdateServiceCategoryDTO(DTOBase):
    id: int
    payload: UpdateServiceCategoryPayload


class DeleteServiceCategoryDTO(DTOBase):
    id: int
