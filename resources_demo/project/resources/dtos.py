from enum import Enum, auto
import datetime
from typing import Optional, TypeVar, Generic, Union
from pydantic import BaseModel, ConfigDict, Field, validator
from core import ActionOnEditableMetadataMixin, CallerDTO, ReportFormats

from lib import DTOBase, Blank, DTOField


SelectionT = TypeVar("SelectionT")
SubDTO_T = TypeVar("SubDTO_T")


# class BaseDTORelationAction(Generic[SelectionT], DTOBase):
    # selection: SelectionT

# class CreateSubs(Generic[SelectionT, SubDTO_T], DTOBase):
    # selection: SelectionT
    # sub_data: SubDTO_T


# class LinkExistingObjects(BaseDTORelationAction[SelectionT], DTOBase):
    # ...


# class UnlinkSubs(BaseDTORelationAction[SelectionT], DTOBase):
    # delete: bool = False


# class AddListElements:
#     ...

# class RemoveListElements:
#     ...


# DefaultDTORelationActions = Union[CreateSubs, LinkExistingObjects, UnlinkSubs]
"""
{
    "selection": {
        "title__ilike": "Hello",
        "id__in": [1, 4, 6],
        "created_at__gt": 15.06.2007,
        "created_at__lt": 15.06.2010
    },
    "payload": {}
}
"""
from pydantic import validator
from lib.interfaces import Expression, OneOrMultuple, BaseSelection, Expressions
T = TypeVar("T")


# TODO: перенести в core
class IdSelection(BaseSelection):
    id: Expressions[int] = Blank

class DateSelection(BaseSelection):
    created_at: Expressions[datetime.datetime] = Blank
    updated_at: Expressions[datetime.datetime] = Blank


# TODO: сделать проверку на то, что хотя бы одно поле заполнено в конечном селекшене


class DefaultMetadataSelection(BaseSelection):
    name: Expressions[str] = Blank
    description: Expressions[str] = Blank
    comments: Expressions[str] = Blank



class ImagesLinks:
    ...


class DocumentsLinks:
    ...


# ______________________________________________________________________________________
from .models import Node

class CreateNodeDTO(DTOBase):
    parent_id: Optional[int] = None

class DeleteNodeDTO(DTOBase):
    id: Optional[int] = Field(default_factory=None)


class UpdateNodeDTO(DTOBase):
    parent_id: DTOField[int] = Blank
    # children: DTOField[list[UnlinkSubs]] = Blank


class RetrieveNodeDTO(IdSelection):
    ...


# множества
class CreateNodesDTO(DTOBase):
    example_name: str
    another_example: Optional[int]


class DeleteNodesDTO(DTOBase):
    ...


class NodesSelection(IdSelection, DateSelection, DefaultMetadataSelection):
    ...


class UpdateNodesPayload(ActionOnEditableMetadataMixin):
    parent_id: DTOField[int] = Blank
    # children: DTOField[list[Union[
    #     CreateSubs[NodesSelection, CreateNodeDTO],
    #     UnlinkSubs[NodesSelection],
    #     LinkExistingObjects[NodesSelection]
    #     ]]] = Blank
    # docs: DTOField[Union[]]
    # images: TODO



class UpdateNodesDTO(DTOBase):
    selection: NodesSelection
    payload: UpdateNodesPayload


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