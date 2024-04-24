import typing

from lib.interfaces import ControllerMixins

from .interfaces import NodesControllerABC, NodesServiceABC
from .dtos import NodesSelection, CreateNodeDTO, UpdateNodesDTO
from .datamappers import NodeDM

from users.interfaces import UserRepoABC


class NodesController(NodesControllerABC,
                      ControllerMixins[
                          NodeDM,
                          CreateNodeDTO,
                          NodesSelection,
                          UpdateNodesDTO,
                          NodesSelection]):
    user_repo: UserRepoABC
    default_service: NodesServiceABC
