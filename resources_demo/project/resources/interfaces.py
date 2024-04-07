from abc import abstractmethod
from archtool.layers.default_layer_interfaces import (
    ABCController,
    ABCService,
    ABCRepo)

from lib.interfaces import RepoMixinsABC
from core import CallerDTO
from .dtos import (CreateNodesDTO,
                   UpdateNodesDTO,
                   DeleteNodesDTO,
                   ListNodesDTO,

                   CreateNodeDTO,
                   RetrieveNodeDTO,
                   UpdateNodeDTO,
                   DeleteNodeDTO)

from .datamappers import NodesDM, NodeDM


class NodesControllerABC(ABCController):
    @abstractmethod
    async def create_multiple(self, data: CreateNodesDTO) -> NodesDM:
        ...

    @abstractmethod
    async def delete_multiple(self, data: DeleteNodesDTO) -> None:
        ...

    @abstractmethod
    async def update_multiple(self, data: UpdateNodesDTO) -> None:
        ...

    @abstractmethod
    async def list_nodes(self, data: ListNodesDTO) -> NodesDM:
        ...


class NodesRepoABC(ABCRepo,
                   RepoMixinsABC[NodeDM,
                                 CreateNodeDTO,
                                 RetrieveNodeDTO,
                                 UpdateNodeDTO,
                                 DeleteNodeDTO]):
    @abstractmethod
    async def list(self, data: ListNodesDTO) -> NodesDM:
        ...
