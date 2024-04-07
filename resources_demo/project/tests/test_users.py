from keycloak import KeycloakAdmin
import pytest
from users.interfaces import UsersControllerABC
from users.dtos import CreateUserDTO, CreateSSOUserDTO

import settings


@pytest.mark.asyncio
async def test_create_user(injector):
    user_controller: UsersControllerABC = injector.get_dependency(key=UsersControllerABC)
    test_user_data = CreateUserDTO(sso_data=dict(username="0nliner", password="12345678"))
    new_user = await user_controller.create_user(data=test_user_data)



async def test_login_as_admin():
    keycloak_admin = KeycloakAdmin(server_url=f"{settings.KC_HOSTNAME}:{settings.KC_PORT}/",
                                   client_id="backend",
                                   client_secret_key="oC9WF3OZnKcEk9PkAMpqZuR82BSnCjY0",
                                   realm_name="backend",
                                   verify=True)
    await keycloak_admin.init_token()
    new_user = {
        "email": "newuser@example.com",
        "username": "newuser",
        "enabled": True,
        "firstName": "New",
        "lastName": "User",
        "credentials": [{
            "type": "password",
            "value": "newuserpassword",
            "temporary": False
        }],
        "realmRoles": ["user_default_roles"],  # Пример назначения ролей
        "attributes": {"custom_attribute": ["custom_value"]}  # Пример добавления пользовательских атрибутов
    }
    # Создание пользователя
    new_user_id = await keycloak_admin.create_user(new_user)
    assert new_user_id
