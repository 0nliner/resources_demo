from lib.interfaces import DMBase


class SSOUserDM(DMBase):
    id: int
    username: str
    phone_number: str
    email: str


class InnerUserDM(DMBase):
    id: int


class UserDM(DMBase):
    sso_user_data: SSOUserDM
    inner_user_data: InnerUserDM
