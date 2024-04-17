from abc import abstractmethod
from archtool.layers.default_layer_interfaces import ABCService
from .dtos import AccessContext


class AccessServiceABC(ABCService):
    @abstractmethod
    def check_role(self, context: AccessContext) -> bool:
        ...

    @abstractmethod
    def is_admin(self, context: AccessContext) -> bool:
        ...

    @abstractmethod
    def is_owner(self, context: AccessContext) -> bool:
        ...

    @abstractmethod
    def is_user(self, context: AccessContext) -> bool:
        ...

    @abstractmethod
    def is_reading_available_fields(self, context: AccessContext) -> bool:
        ...

    @abstractmethod
    def during_business_hours(self, context: AccessContext) -> bool:
        ...
