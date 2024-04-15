from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from .dtos import (ListNodesDTO,
                   CreateNodeDTO,
                   RetrieveNodeDTO,
                   UpdateNodeDTO,
                   DeleteNodeDTO,
                   UploadImageDTO)
from .models import Node
from .datamappers import NodesDM, NodeDM, ImageDM
from .interfaces import NodesRepoABC
from lib.interfaces import RepoMixins


class NodesRepo(NodesRepoABC,
                RepoMixins[NodeDM,
                           CreateNodeDTO,
                           RetrieveNodeDTO,
                           UpdateNodeDTO,
                           DeleteNodeDTO]):
    model = Node
    session_maker: sessionmaker
    
    async def list(self, data: ListNodesDTO) -> NodesDM:
        ...

    async def upload_image(self, data: UploadImageDTO) -> ImageDM:
        ...
