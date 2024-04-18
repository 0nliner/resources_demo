from abc import abstractmethod
import typing

from archtool.layers.default_layer_interfaces import ABCService, ABCController

from .dtos import AccessContext
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
