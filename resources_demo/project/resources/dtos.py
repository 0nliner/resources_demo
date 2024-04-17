import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from core import CallerDTO, ReportFormats


class CreateNodeDTO(BaseModel):
    parent_id: Optional[int] = Field(default_factory=None)


class DeleteNodeDTO(BaseModel):
    id: Optional[int] = Field(default_factory=None)


class UpdateNodeDTO(BaseModel):
    ...

class RetrieveNodeDTO(BaseModel):
    id: int


# множества
class CreateNodesDTO(BaseModel):
    example_name: str
    another_example: Optional[int]


class DeleteNodesDTO(BaseModel):
    ...


class UpdateNodesDTO(BaseModel):
    ...


class ListNodesDTO(BaseModel):
    caller: CallerDTO


class UploadImageDTO(BaseModel):
    ...


class CreateBidDTO(BaseModel):
    ...


class BidDTO(BaseModel):
    id: int
    subject_id: str
    status_id: str
    responsible_id: int
    planned_start: datetime.datetime
    planned_end: datetime.datetime
    actual_start: datetime.datetime
    actual_end: datetime.datetime
    initiator_id: int
    initiator_comments: str
    executor_id: int
    created_at: datetime.datetime


class CreateReportDTO(BaseModel):
    format_type: ReportFormats
    # дата объектов, участвующих в формировании за временной период
    period_start: Optional[datetime.datetime]
    period_end: Optional[datetime.datetime]

    bid: BidDTO
    # format_by:
    created_at: datetime.datetime
    done_at: datetime.datetime


# заявка
# модуль - service_requests


# услуга - Service, лежит в services
# shop не используется
# подтягивать ли ещё ServiceLayoutPattern


# 
# формирова