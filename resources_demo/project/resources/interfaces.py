from abc import abstractmethod
from archtool.layers.default_layer_interfaces import (
    ABCController,
    ABCService,
    ABCRepo)

from lib.interfaces import (
    RepoMixinsABC,
    ControllerMixinsABC,
    ServiceMixinsABC)

from core import CallerDTO, ReportFormats
from .dtos import (NodesSelection,
                   UpdateNodesDTO,
                   CreateNodeDTO)

from .datamappers import NodeDM


class NodesControllerABC(ABCController,
                         ControllerMixinsABC[
                                 NodeDM,
                                 CreateNodeDTO,
                                 NodesSelection,
                                 UpdateNodesDTO,
                                 NodesSelection]):
    ...


class NodesServiceABC(ABCService,
                      ServiceMixinsABC[
                                NodeDM,
                                CreateNodeDTO,
                                NodesSelection,
                                UpdateNodesDTO,
                                NodesSelection]):
    ...


class NodesRepoABC(ABCRepo,
                   RepoMixinsABC[
                       NodeDM,
                       CreateNodeDTO,
                       NodesSelection,
                       UpdateNodesDTO,
                       NodesSelection]):
    ...


# class ReportControllerABC(ABCController):
#     @abstractmethod
#     async def generate_report(data: CreateReportDTO):
#         ...
