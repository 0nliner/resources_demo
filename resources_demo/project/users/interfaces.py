from abc import abstractmethod
from archtool.layers.default_layer_interfaces import ABCController, ABCService, ABCRepo
from core import CallerDTO
from lib.interfaces import ControllerMixinsABC, RepoMixinsABC, ServiceMixinsABC

from .dtos import (CreateInnerUserDTO,
                   CreateUserDTO,
                   DeleteInnerUserDTO,
                   RetrieveInnerUserDTO,
                   UpdateInnerUserDTO)

from .datamappers import UserDM, SSOUserDM, InnerUserDM


class UsersControllerABC(ABCController,
                         ControllerMixinsABC[
                           InnerUserDM,
                           CreateInnerUserDTO,
                           RetrieveInnerUserDTO,
                           UpdateInnerUserDTO,
                           DeleteInnerUserDTO]):
    ...


class SSORepoABC(ABCRepo):
    @abstractmethod
    async def get_user(self) -> SSOUserDM:
        ...

    @abstractmethod
    async def create_user(self, data: CreateUserDTO) -> SSOUserDM:
        ...


class UserServiceABC(ABCService,
                     ServiceMixinsABC[
                       InnerUserDM,
                       CreateInnerUserDTO,
                       RetrieveInnerUserDTO,
                       UpdateInnerUserDTO,
                       DeleteInnerUserDTO]):
    ...

# UserServiceABC.retrieve

class UserRepoABC(ABCRepo,
                  RepoMixinsABC[InnerUserDM,
                                CreateInnerUserDTO,
                                RetrieveInnerUserDTO,
                                UpdateInnerUserDTO,
                                DeleteInnerUserDTO]):
    ...


# class AuthServiceABC(ABCService):
#     @abstractmethod
#     def can_perform_action(self, caller: CallerDTO, action) -> bool:
#         ...
