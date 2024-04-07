from pydantic import BaseModel


class SSOUserDM(BaseModel):
    id: int
    username: str
    phone_number: str
    email: str


class InnerUserDM(BaseModel):
    id: int


class UserDM(BaseModel):
    sso_user_data: SSOUserDM
    inner_user_data: InnerUserDM
