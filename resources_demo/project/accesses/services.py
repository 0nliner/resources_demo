import typing
from dataclasses import dataclass
from pydantic import BaseModel
from archtool.layers.default_layer_interfaces import ABCController
from core import CallerDTO

from users.interfaces import UserServiceABC
from users.dtos import RetrieveInnerUserDTO

from .interfaces import AccessServiceABC, PolicyRepoABC
from .datamappers import PolicyDM
from .dtos import AccessContext
from lib.interfaces import get_dto_and_dm, resolve_controller_name


POLICES = []


class AccessService(AccessServiceABC):
    user_service: UserServiceABC
    policy_repo: PolicyRepoABC

    async def is_accesible(self,
                           caller: CallerDTO,
                           action: typing.Callable) -> bool:
        """
        action - метод контроллера
        """
        dto, datamapper = get_dto_and_dm(action)

        controller: ABCController = None
        # обработка для дженериков
        if hasattr(action, "__self__"):
            controller = type(action.__self__)
        else:
            controller = action.__class__

        # TODO: делаем проверку по полям dto
        # self.get_roles_for_dto()
        context = AccessContext(caller=caller, dto=dto)
        # TODO: нужно получить инфу о политиках на контроллер, затем их проитерировать
        controller_polices = await self.policy_repo.get_polices_by_controller_name(
            controller_name=resolve_controller_name(controller))

        for policy in controller_polices:
            policy_decision = await self.is_policy_allows(policy=policy, context=context)
            if not policy_decision:
                return False
        return True

    async def is_policy_allows(self,
                               policy: PolicyDM,
                               context: AccessContext) -> bool:
        for condition in policy.conditions:
            if not condition(context):
                return False
        return True

    async def get_roles_for_dto(self, model_name: str):
        """
        скорее всего будет ходить в бэк, в котором описаны роли под дто,
        хотя сам механизм ролей является неполным механизмом авторизации
        """
        ...

    async def get_controller_polices(self):
        ...

    # -----------------------------------------------------------------------------------------
    async def check_role(self, context: AccessContext) -> bool:
        user = await self.user_service.retrieve(id=context.caller.id)

    async def is_admin(self, context: AccessContext) -> bool:
        user = await self.user_service.retrieve(data=RetrieveInnerUserDTO(id=context.caller.id))
        return user.role == 'admin'

    async def is_owner(self, context: AccessContext) -> bool:
        user = await self.user_service.retrieve(data=RetrieveInnerUserDTO(id=context.caller.id))
        return user.id == context.get('resource_owner_id')

    async def is_user(self, context: AccessContext) -> bool:
        user = await self.user_service.retrieve(data=RetrieveInnerUserDTO(id=context.caller.id))
        return user.role == context.caller.role_id

    async def is_acting_on_available_fields(self, context: AccessContext) -> bool:
        context.dto

    async def during_business_hours(self, context) -> bool:
        from datetime import datetime
        current_hour = datetime.now().hour
        return 9 <= current_hour <= 17
