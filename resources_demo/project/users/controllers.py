from users.datamappers import UserDM
from users.dtos import CreateUserDTO, CreateInnerUserDTO
from .interfaces import UsersControllerABC, SSORepoABC, UserRepoABC


class UserController(UsersControllerABC):
    sso_repo: SSORepoABC
    users_repo: UserRepoABC

    async def create_user(self, data: CreateUserDTO) -> UserDM:
        # TODO: перенести эту логику в сервисы
        # TODO: что с соблюдением ACID ?
        new_sso_user = await self.sso_repo.create_user(data=data.sso_data)
        inner_user_data = CreateInnerUserDTO(id=new_sso_user.id)
        new_inner_user = await self.users_repo.create(data=inner_user_data)
        user_dm = UserDM(sso_user_data=new_sso_user,
                         inner_user_data=new_inner_user)
        return user_dm

    async def list_users(self, data) -> list[UserDM]:
        ...
