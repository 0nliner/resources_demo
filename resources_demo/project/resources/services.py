from lib.interfaces import ServiceMixins

from .dtos import (CreateNodeDTO, NodesSelection, UpdateNodesDTO)
from .datamappers import NodeDM
from .interfaces import NodesServiceABC


class NodesService(NodesServiceABC,
                   ServiceMixins[
                       NodeDM,
                       CreateNodeDTO,
                       NodesSelection,
                       UpdateNodesDTO,
                       NodesSelection]):

    default_repo: NodesServiceABC
