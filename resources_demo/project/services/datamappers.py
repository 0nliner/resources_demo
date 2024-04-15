from typing import Optional
import datetime
from uuid import UUID
from pydantic import BaseModel


class ServiceDM(BaseModel):
    id: UUID
    title: str
    short_description: str
    long_description: str
    publication_date: datetime.datetime
    service_category: UUID
    provider_company: UUID
    is_active: bool
    is_internal: bool
    image_url: str
    image_thumbnail_url: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    employees: list[UUID]
    # reporting: "no_report"
    # нло
    #   sort_order: int
    #   grid_width: int
    #   realty_object_types: list[UUID]
    #   residences: list[UUID]


class ServiceCategoryDM(BaseModel):
    id: UUID
    title: Optional[str]
    is_active: Optional[bool]
    icon_tag: Optional[str]
    created_at: datetime.Optional[datetime]
    updated_at: datetime.Optional[datetime]
    # опционально
    services_ids: Optional[list[int]]
    service_count: Optional[int]

