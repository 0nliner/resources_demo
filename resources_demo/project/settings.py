import os

POSTGRES_HOST = "0.0.0.0"
POSTGRES_PORT = "6007"
POSTGRES_USER = "test_user"
POSTGRES_PASSWORD = "test_user"
POSTGRES_DB = "test_db"
DB_URL = r"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
             user=POSTGRES_USER,
             password=POSTGRES_PASSWORD,
             host=POSTGRES_HOST,
             port=POSTGRES_PORT,
             database=POSTGRES_DB
            )


KC_HOSTNAME = os.getenv("KC_HOSTNAME")
KC_PORT = os.getenv("KC_PORT")
KC_REALM_NAME = os.getenv("KC_REALM_NAME")
KC_LOG_LEVEL = os.getenv("KC_LOG_LEVEL")
KEYCLOAK_ADMIN = os.getenv("KEYCLOAK_ADMIN")
KEYCLOAK_ADMIN_PASSWORD = os.getenv("KEYCLOAK_ADMIN_PASSWORD")
KC_SECRET_KEY = os.getenv("KC_SECRET_KEY")

# для того чтобы зайти в админку keycloak
# http://0.0.0.0:8080/realms/master/protocol/openid-connect/auth?client_id=security-admin-console&redirect_uri=http%3A%2F%2F0.0.0.0%3A8080%2Fadmin%2Fmaster%2Fconsole%2F&state=3bbc0a7f-d4d2-48c6-8970-d4b9f1b2f40c&response_mode=fragment&response_type=code&scope=openid&nonce=df4a7649-48d5-46c8-bbcc-54440b73ee68&code_challenge=rADxNIx4wjnsq2iZ4BwcuzOktS0TMcZXVwfWTWUuDuE&code_challenge_method=S256
AWS_ACCESS_KEY_ID = os.getenv('your_access_key')
AWS_SECRET_ACCESS_KEY = os.getenv('your_secret_key')
REGION_NAME = os.getenv('your_region')
BUCKET_NAME = os.getenv('your_bucket_name')
FILE_NAME = os.getenv('your_file_name')


