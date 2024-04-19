import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from core import CallerDTO, ReportFormats

from lib import DTOBase


class CreateNodeDTO(DTOBase):
    parent_id: Optional[int] = Field(default_factory=None)


class DeleteNodeDTO(DTOBase):
    id: Optional[int] = Field(default_factory=None)


class UpdateNodeDTO(DTOBase):
    ...

class RetrieveNodeDTO(DTOBase):
    id: int


# множества
class CreateNodesDTO(DTOBase):
    example_name: str
    another_example: Optional[int]


class DeleteNodesDTO(DTOBase):
    ...


class UpdateNodesDTO(DTOBase):
    ...


class ListNodesDTO(DTOBase):
    caller: CallerDTO


class UploadImageDTO(DTOBase):
    ...


class CreateBidDTO(DTOBase):
    ...


class BidDTO(DTOBase):
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


class CreateReportDTO(DTOBase):
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