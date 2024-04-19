from users.interfaces import UsersControllerABC

from accesses.interfaces import PolicyRepoABC
from accesses.dtos import CreatePolicyDTO

"""
План тестирования:
 - проверить работу мидлвера авторизации
 - проверить работоспособность GET, POST, PATCH, DELETE методов
"""


async def test_policy_middleware(injector, api_client, clean_test_session):
    # TODO: создать тестовые политики, проверить что правильно отрабатывают
    # TODO: проконтролировать что для запроса пользователя правильно создаётся AccessContext (там не хватает логики)
    access_service = 
    all_checks = ...
    checks

    polices = [
        dict(policy_on=UsersControllerABC.create, policy_data=dict(role_id=1), conditions=checks)
    ]

    policy_repo: PolicyRepoABC = injector.get_dependency(PolicyRepoABC)
    for policy in polices:
        new_policy = await policy_repo.create(data=CreatePolicyDTO(**policy),
                                              session=clean_test_session)
    # тут запрос
    # тут проверка


async def test_aiohttp_generated_api(injector, api_client, aiohttp_app):
    # TODO: тут нужно придумать что-то поумнее
    response_1 = await api_client.get("/api/user/1")
    assert response_1
