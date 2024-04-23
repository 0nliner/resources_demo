from abc import abstractmethod
from archtool.layers.default_layer_interfaces import (
    ABCController,
    ABCService,
    ABCRepo)

from lib.interfaces import RepoMixinsABC, OneOrMultuple
from core import CallerDTO, ReportFormats
from .dtos import (CreateNodesDTO, NodesSelection,
                   UpdateNodesDTO,
                   DeleteNodesDTO,
                   ListNodesDTO,

                   CreateNodeDTO,
                   RetrieveNodeDTO,
                   UpdateNodeDTO,
                   DeleteNodeDTO,
                   CreateReportDTO)

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
                                 NodesSelection,
                                 UpdateNodesDTO,
                                 NodesSelection]):
    @abstractmethod
    async def list(self, data: ListNodesDTO) -> NodesDM:
        ...


# class ReportControllerABC(ABCController):
#     @abstractmethod
#     async def generate_report(data: CreateReportDTO):
#         ...
