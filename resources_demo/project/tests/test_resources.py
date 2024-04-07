import typing
import pytest
from archtool.dependecy_injector import DependecyInjector

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from resources.interfaces import NodesRepoABC
from resources.dtos import CreateNodeDTO, RetrieveNodeDTO
from resources.datamappers import NodeDM


# TODO: сработает ли на этом говне роллбэк ? (разные сессии по идее получаются)
# может стоит хранить сессиии в contextvar ?
@pytest.fixture
async def test_node(injector):
    nodes_repo: NodesRepoABC = injector.get_dependency(key=NodesRepoABC)
    create_node_data = CreateNodeDTO()
    new_node = await nodes_repo.create(data=create_node_data,
                                       commit=True)
    return new_node


@pytest.mark.asyncio
async def test_create_node(injector, clean_test_session):
    nodes_repo: NodesRepoABC = injector.get_dependency(key=NodesRepoABC)
    create_node_data = CreateNodeDTO()
    new_node = await nodes_repo.create(data=create_node_data,
                                       commit=True,
                                       session=clean_test_session)
    assert new_node


@pytest.mark.asyncio
async def test_retrieve_node(injector, test_node: NodeDM, clean_test_session):
    nodes_repo: NodesRepoABC = injector.get_dependency(key=NodesRepoABC)
    retrieve_node_data = RetrieveNodeDTO(id=test_node.id)
    node = await nodes_repo.retrieve(data=retrieve_node_data, session=clean_test_session)
    assert node

