from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from .dtos import (ListNodesDTO,
                   UpdateNodesDTO,
                   CreateNodeDTO,
                   NodesSelection,
                   UploadImageDTO)
from .models import Node
from .datamappers import NodesDM, NodeDM, ImageDM
from .interfaces import NodesRepoABC
from lib.interfaces import RepoMixins, OneOrMultuple


class NodesRepo(NodesRepoABC,
                RepoMixins[NodeDM,
                           CreateNodeDTO,
                           NodesSelection,
                           UpdateNodesDTO,
                           NodesSelection]):
    model = Node
    session_maker: sessionmaker
    
    async def list(self, data: ListNodesDTO) -> NodesDM:
        ...

    async def upload_image(self, data: UploadImageDTO) -> ImageDM:
        ...
