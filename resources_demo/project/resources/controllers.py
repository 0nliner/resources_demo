from .interfaces import NodesControllerABC
from .dtos import CreateNodesDTO, UpdateNodesDTO, DeleteNodesDTO, ListNodesDTO
from .datamappers import NodesDM

from users.interfaces import UserRepoABC

class NodesController(NodesControllerABC):
    user_repo: UserRepoABC

    async def create_multiple(self, data: CreateNodesDTO) -> NodesDM:
        ...

    async def delete_multiple(self, data: DeleteNodesDTO) -> None:
        ...

    async def update_multiple(self, data: UpdateNodesDTO) -> None:
        ...

    async def list_nodes(self, data: ListNodesDTO) -> NodesDM:
        # пытаемся найти объект пользователя в локальной таблице
        await self.user_repo.get(data.caller)
