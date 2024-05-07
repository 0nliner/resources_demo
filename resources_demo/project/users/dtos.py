from typing import Optional, Union, TypeVar
from pydantic import BaseModel, ConfigDict
from lib import DTOBase

from lib import Blank, DTOField, DTOBase


class CreateInnerUserDTO(DTOBase):
    id: int


class RetrieveInnerUserDTO(DTOBase):
    id: DTOField[int] = Blank
    role_id: DTOField[int] = Blank
    role: DTOField[str] = Blank


class UpdateInnerUserDTO(DTOBase):
    example: str


class DeleteInnerUserDTO(DTOBase):
    example: str


# SSO
class CreateSSOUserDTO(DTOBase):
    username: str
    password: str


# services and controllers dtos
class CreateUserDTO(DTOBase):
    sso_data: CreateSSOUserDTO    
    # TODO: other fields


class GetUserDTO(DTOBase):
    id: Optional[int]
    username: Optional[str]
