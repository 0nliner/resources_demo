import asyncio
from aiohttp import web
import aiobotocore.session
from archtool.dependecy_injector import DependecyInjector
from archtool.global_types import AppModule

import aiobotocore
from keycloak import KeycloakAdmin, KeycloakOpenID
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core import Base
from utils import create_tables
from lib.interfaces import ArchtoolsAPIGenerator, ArchtoolsOpenApiGenerator

import settings


# 
# async def upload_file_to_s3():
#     session = aiobotocore.get_session()
#     async with session.create_client('s3', region_name=REGION_NAME,
#                                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
#                                       aws_access_key_id=AWS_ACCESS_KEY_ID) as client:
#         # Загрузка файла
#         with open(FILE_NAME, 'rb') as file_data:
#             await client.put_object(Bucket=BUCKET_NAME, Key=FILE_NAME, Body=file_data)
#         print(f'{FILE_NAME} has been uploaded to {BUCKET_NAME}')

from dataclasses import dataclass

@dataclass
class Dependency:
    key: object
    value: object


def init_deps(injector: DependecyInjector):
    """
    регистрируем необходимые зависимости
    """
    # TODO: сделать автопоиск зависимостей по модулям
    engine = create_async_engine(settings.DB_URL, echo=True)
    session_maker = sessionmaker(bind=engine,
                                 class_=AsyncSession,
                                 expire_on_commit=False)

    injector._reg_dependecy(AsyncEngine, engine)
    injector._reg_dependecy(sessionmaker[AsyncSession], session_maker)
    # keycloak
    keycloak_data = dict(
        server_url=f"{settings.KC_HOSTNAME}:{settings.KC_PORT}/",
        client_id="backend",
        realm_name="backend",
        client_secret_key="DwOtH7ETrIcvXibIfH0StkSYHErMkh6s"
    )
    keycloak_admin_data = dict(
                            server_url=f"{settings.KC_HOSTNAME}:{settings.KC_PORT}/",
                            realm_name="backend",
                            username="admin",
                            password="keycloak",
                            client_id="admin-cli",
                            client_secret_key="iS3RfjlGdRljf1RBnspilzNf7TZxygAO")
    injector._reg_dependecy(KeycloakOpenID, KeycloakOpenID(**keycloak_data))
    injector._reg_dependecy(KeycloakAdmin, KeycloakAdmin(**keycloak_admin_data))
    # s3
    s3_session = aiobotocore.session.get_session()
    s3_client = s3_session.create_client('s3',
                                         region_name=settings.REGION_NAME,
                                         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                         aws_access_key_id=settings.AWS_ACCESS_KEY_ID)
    injector._reg_dependecy(aiobotocore.session.AioSession, s3_session)
    injector._reg_dependecy(aiobotocore.session.ClientCreatorContext, s3_client)

import pathlib
from accesses.interfaces import AccessServiceABC
from core import CallerDTO


def policies_authorization(injector: DependecyInjector):
    def wrapped(caller: CallerDTO, request):
        access_service = injector.get_dependency(AccessServiceABC)
    return wrapped


def init(loop, run: bool = False):
    import sys
    # sys.path.insert(0, "")
    loop = asyncio.get_event_loop()
    modules = [AppModule("resources"),
               AppModule("users"),
               AppModule("accesses"),
               AppModule("devices")]

    injector = DependecyInjector(modules_list=modules)
    init_deps(injector)

    injector.inject()
    api_generator = ArchtoolsAPIGenerator(injector,
                                          custom_midlewares=[policies_authorization(injector=injector)])
    
    app = api_generator.aiohttp_app(loop=loop)
    app._middlewares.append()
    openapi_generator = ArchtoolsOpenApiGenerator(injector=injector)
    openapi_generator.generate_openapi(dest_folder=pathlib.Path.cwd() / "openapi")

    tasks = (
        create_tables(engine=injector.get_dependency(AsyncEngine), base=Base),
    )

    for task in tasks:
        loop.run_until_complete(task)
    return injector, app


if __name__ == "__main__":
    EVENT_LOOP_POLICY = asyncio.get_event_loop_policy()
    EVENT_LOOP = asyncio.new_event_loop()
    EVENT_LOOP_POLICY.set_event_loop(EVENT_LOOP)

    injector, app = init(run=True, loop=EVENT_LOOP)
    web.run_app(app, port=8083, loop=EVENT_LOOP)
