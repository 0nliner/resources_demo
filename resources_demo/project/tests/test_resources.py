import typing
import pytest
from archtool.dependecy_injector import DependecyInjector

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from resources.interfaces import NodesRepoABC
from resources.dtos import *
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

@pytest.fixture
async def test_nodes_structure(injector, clean_test_session):
    nodes_repo: NodesRepoABC = injector.get_dependency(key=NodesRepoABC)
    # создадим небольшую иерархию ресурсов
    root_node = await nodes_repo.create(data=CreateNodeDTO(), session=clean_test_session, commit=True)
    childs_ids = []
    for i in range(10):
        create_child_node_dto = CreateNodeDTO(parent_id=root_node.id)
        new_node = await nodes_repo.create(data=create_child_node_dto, session=clean_test_session, commit=True)
        childs_ids.append(new_node.id)
    return [root_node, *childs_ids]



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
    retrieve_node_data = NodesSelection(id__in_=[test_node.id, 1000])
    node = await nodes_repo.retrieve(data=retrieve_node_data, session=clean_test_session)
    assert node


@pytest.mark.asyncio
async def test_update_nodes(injector, clean_test_session, test_nodes_structure):
    nodes_repo: NodesRepoABC = injector.get_dependency(key=NodesRepoABC)
    childs_ids = test_nodes_structure[1:]
    # проверим обновление данных
    update_node_data = UpdateNodesDTO(selection=NodesSelection(id__in_=childs_ids),
                                      payload=UpdateNodesPayload(comments="10"))
    nodes = await nodes_repo.update(data=update_node_data, session=clean_test_session)

    assert len(nodes) == len(childs_ids)

    for node in nodes:
        assert node.comments

    await clean_test_session.commit()
    assert nodes


@pytest.mark.asyncio
async def test_delete_nodes(injector, clean_test_session, test_nodes_structure):
    childs_ids = test_nodes_structure[1:]
    nodes_repo: NodesRepoABC = injector.get_dependency(key=NodesRepoABC)
    delete_nodes_selection = NodesSelection(id__in_=childs_ids)
    result = await nodes_repo.delete(data=delete_nodes_selection, session=clean_test_session) #, commit=True
    assert result


@pytest.mark.asyncio
async def test_list_nodes(injector, clean_test_session, test_nodes_structure):
    ...


# TODO: сериализация списка с моделями
# json.dumps(users, default=pydantic_encoder))

# премер с обновлением поля родителя у списка нод
# UpdateNodesDTO(selection=NodesSelection(ids=[1, 3, 5, 7]), payload=UpdateNodesPayload(parent_id=None))
# пример отвязки от конкретной ноды других нод
# UpdateNodesDTO(selection=NodesSelection(ids=[1]),
            #    payload=UpdateNodesPayload(
                #    children=[UnlinkSubs(
                    #    selection=NodesSelection(ids=[10]))]))
# как выглядит при этом json

# TODO
# пример привязки к ноде документов
# UpdateNodesDTO(selection=NodesSelection(ids=[1]),
            #    payload=UpdateNodesPayload())
