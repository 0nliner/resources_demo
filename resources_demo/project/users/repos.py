from typing import Optional

from keycloak import KeycloakAdmin, KeycloakOpenID
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from lib.interfaces import RepoMixins

from .interfaces import SSORepoABC, UserRepoABC
from .dtos import (# sso   
                   CreateSSOUserDTO,
                   # inner user  
                   CreateInnerUserDTO,
                   RetrieveInnerUserDTO,
                   UpdateInnerUserDTO,
                   DeleteInnerUserDTO)

from .datamappers import InnerUserDM
from .models import User


class KeycloakRepo(SSORepoABC):
    keycloak_client: KeycloakOpenID
    keycloak_admin: KeycloakAdmin

    async def get_user(self):
        await keycloak_openid.userinfo(token['access_token'])

    async def authorize_user(self, username: str, password: str) -> dict:
        self.keycloak_client.token(username=settings.KEYCLOAK_ADMIN,
                                   password=settings.KEYCLOAK_ADMIN_PASSWORD)

    async def create_user(self, data: CreateSSOUserDTO):
        await self.keycloak_admin.init_token()
        new_user = await self.keycloak_admin.create_user(**data)

class UserRepo(UserRepoABC,
               RepoMixins[InnerUserDM,
                          CreateInnerUserDTO,
                          RetrieveInnerUserDTO,
                          UpdateInnerUserDTO,
                          DeleteInnerUserDTO]):

    model = User
    session_maker: sessionmaker
