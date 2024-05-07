from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID

from lib import DTOBase, Blank

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


class UpdateServicePayload(DTOBase):
    title: Optional[str] = Blank
    short_description: Optional[str] = Blank
    long_description: Optional[str] = Blank
    service_category: Optional[UUID] = Blank
    is_active: Optional[bool] = Blank
    is_internal: Optional[bool] = Blank
    image_url: Optional[str] = Blank
    image_thumbnail_url: Optional[str] = Blank


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


class UpdateServiceCategoryPayload(DTOBase):
    title: Optional[str]
    is_active: Optional[bool]
    icon_tag: Optional[str]


class UpdateServiceCategoryDTO(DTOBase):
    id: int
    payload: UpdateServiceCategoryPayload


class DeleteServiceCategoryDTO(DTOBase):
    id: int
