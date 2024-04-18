from typing import Optional
from pydantic import BaseModel


class CreateInnerUserDTO(BaseModel):
    id: int


class RetrieveInnerUserDTO(BaseModel):
    id: Optional[int] = None
    role_id: Optional[int] = None
    role: Optional[str] = None


class UpdateInnerUserDTO(BaseModel):
    ...


class DeleteInnerUserDTO(BaseModel):
    ...


# SSO
class CreateSSOUserDTO(BaseModel):
    username: str
    password: str


# services and controllers dtos
class CreateUserDTO(BaseModel):
    sso_data: CreateSSOUserDTO    
    # TODO: other fields


class GetUserDTO(BaseModel):
    id: Optional[int]
    username: Optional[str]
