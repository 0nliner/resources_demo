import asyncio
from archtool.dependecy_injector import DependecyInjector
from archtool.global_types import AppModule

from keycloak import KeycloakAdmin, KeycloakOpenID
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core import Base
from utils import create_tables

import settings


def init():
    import sys
    sys.path.insert(0, "")
    loop = asyncio.get_event_loop()
    modules = [AppModule("resources"),
               AppModule("users")]

    injector = DependecyInjector(modules_list=modules)
    engine = create_async_engine(settings.DB_URL, echo=True)
    session_maker = sessionmaker(bind=engine,
                                 class_=AsyncSession,
                                 expire_on_commit=False)
    # регистрируем необходимые зависимости
    # TODO: сделать автопоиск зависимостей по модулям
    injector._reg_dependecy(AsyncEngine, engine)
    injector._reg_dependecy(sessionmaker[AsyncSession], session_maker)

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
    injector.inject()

    
    tasks = (
        create_tables(engine=engine, base=Base),
    )
    
    for task in tasks:
        loop.run_until_complete(task)
    return injector


if __name__ == "__main__":
    injector = init()
