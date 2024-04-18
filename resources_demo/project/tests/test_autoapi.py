"""
План тестирования:
 - проверить работу мидлвера авторизации
 - проверить работоспособность GET, POST, PATCH, DELETE методов
"""

async def test_aiohttp_generated_api(injector, api_client, aiohttp_app):
    response_1 = await api_client.get("/api/user/1")
    assert response_1
