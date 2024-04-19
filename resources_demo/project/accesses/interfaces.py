from abc import abstractmethod
import typing

from sqlalchemy.ext.asyncio import AsyncSession
from archtool.layers.default_layer_interfaces import ABCService, ABCController, ABCRepo
from pydantic import TypeAdapter

from .datamappers import *
from .dtos import *
from lib.interfaces import RepoMixinsABC
from core import CallerDTO


class AccessServiceABC(ABCService):
    # TODO: является ли нарушением слоёв использование атрибута contorller ?
    # сервис по сути является частью обслуживающей инфраструктуры
    # место на подумать 
    @abstractmethod
    async def is_accesible(self,
                           caller: CallerDTO,
                           action: typing.Callable) -> bool:
        ...

    @abstractmethod
    async def is_policy_allows(self,
                               policy,
                               context: AccessContext) -> bool:
        ...

    @abstractmethod
    async def get_roles_for_dto(self, model_name: str):
        ...

    @abstractmethod
    async def check_role(self, context: AccessContext) -> bool:
        ...

    @abstractmethod
    async def get_roles_for_dto(self, model_name: str):
        ...

    @abstractmethod
    async def is_admin(self, context: AccessContext) -> bool:
        ...

    @abstractmethod
    async def is_owner(self, context: AccessContext) -> bool:
        ...

    @abstractmethod
    async def is_user(self, context: AccessContext) -> bool:
        ...

    @abstractmethod
    async def is_acting_on_available_fields(self, context: AccessContext) -> bool:
        ...

    @abstractmethod
    async def during_business_hours(self, context: AccessContext) -> bool:
        ...


class PolicyRepoABC(ABCRepo,
                    RepoMixinsABC[
                        PolicyDM,
                        CreatePolicyDTO,
                        RetrievePolicyDTO,
                        UpdatePolicyDTO,
                        DeletePolicyDTO]):
    
    @abstractmethod
    async def get_polices_by_controller_name(self,
                                             controller_name: str,
                                             session: Optional[AsyncSession] = None
                                             ) -> list[PolicyDM]:
        ...
