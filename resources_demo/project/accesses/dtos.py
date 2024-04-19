from typing import Optional
from dataclasses import dataclass
from pydantic import BaseModel

from lib import DTOBase
from core import CallerDTO


@dataclass
class AccessContext:
    dto: BaseModel
    caller: CallerDTO


class CreatePolicyDTO(DTOBase):
    policy_on: str
    policy: Optional[dict]
    conditions: list[str]


class RetrievePolicyDTO(DTOBase):
    id: Optional[int]
    policy_on: Optional[str]
    conditions: list[str]


class UpdatePolicyPayload(BaseModel):
    policy_on: Optional[str]
    policy: Optional[dict]
    conditions: list[str]


class UpdatePolicyDTO(DTOBase):
    payload: UpdatePolicyPayload


class DeletePolicyDTO(DTOBase):
    id: int
