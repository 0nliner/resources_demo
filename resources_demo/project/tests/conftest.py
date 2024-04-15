import typing
import asyncio
from pytest import fixture
import pytest

import sys
import pathlib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from archtool.dependecy_injector import DependecyInjector

sys.path.insert(0, "/home/merlin/code/resources/resources_demo/project")
sys.path.insert(0, "")

from app import init
from resources.interfaces import NodesRepoABC
from resources.dtos import CreateNodeDTO


EVENT_LOOP_POLICY = asyncio.get_event_loop_policy()
EVENT_LOOP = asyncio.new_event_loop()
EVENT_LOOP_POLICY.set_event_loop(EVENT_LOOP)


@fixture(scope="session")
def event_loop():
    return EVENT_LOOP


def pytest_sessionfinish(session, exitstatus):
    EVENT_LOOP.close()


@fixture(scope="module")
def injector(event_loop):
    injector = init(loop=event_loop)
    return injector


# TODO: думаю лучше записывать сессию в contextvar, сессию брать оттуда же
@pytest.fixture(scope="function")
async def clean_test_session(injector: DependecyInjector):
    session_maker = typing.cast(sessionmaker[AsyncSession], injector.get_dependency(key=sessionmaker))
    async with session_maker() as session:
        yield session
        await session.rollback()

# @pytest.fixture(scope="function")
# async def clean_test_session(injector: DependecyInjector):
#     session_maker = typing.cast(sessionmaker[AsyncSession], injector.get_dependency(key=sessionmaker))
#     async with session_maker() as session:
#         yield session
#         await session.rollback()
