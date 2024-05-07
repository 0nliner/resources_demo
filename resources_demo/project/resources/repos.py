from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from lib.interfaces import RepoMixins

from .dtos import (UpdateNodesDTO,
                   CreateNodeDTO,
                   NodesSelection,
                   UploadImageDTO)

from .models import Node
from .datamappers import NodeDM
from .interfaces import NodesRepoABC


class NodesRepo(NodesRepoABC,
                RepoMixins[NodeDM,
                           CreateNodeDTO,
                           NodesSelection,
                           UpdateNodesDTO,
                           NodesSelection]):
    model = Node
    session_maker: sessionmaker

    # async def upload_image(self, data: UploadImageDTO) -> ImageDM:
    #     ...
