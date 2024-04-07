import typing

from .interfaces import NodesControllerABC, APIController
from .dtos import CreateNodesDTO, UpdateNodesDTO, DeleteNodesDTO, ListNodesDTO
from .datamappers import NodesDM

from users.interfaces import UserRepoABC
from lib.interfaces import BaseAPIController


class NodesController(NodesControllerABC, BaseAPIController):
    user_repo: UserRepoABC

    async def create_multiple(self, data: CreateNodesDTO) -> NodesDM:
        await self.user_repo.create_multiple(data.caller)

    async def delete_multiple(self, data: DeleteNodesDTO) -> None:
        await self.user_repo.delete_multiple(data.caller)

    async def update_multiple(self, data: UpdateNodesDTO) -> None:
        await self.user_repo.update_multiple(data.caller)

    async def list_nodes(self, data: ListNodesDTO) -> NodesDM:
        # пытаемся найти объект пользователя в локальной таблице
        await self.user_repo.get(data.caller)
