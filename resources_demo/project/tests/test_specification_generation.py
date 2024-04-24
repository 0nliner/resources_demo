import pathlib
from archtool.dependecy_injector import DependecyInjector
from lib.interfaces import ArchtoolsOpenApiGenerator


def test_generate_openapi(injector: DependecyInjector):
    openapi_generator = ArchtoolsOpenApiGenerator(injector=injector)
    result = openapi_generator.generate_openapi(dest_file=pathlib.Path.cwd() / "openapi.yaml")

