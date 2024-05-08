from pathlib import Path
from archtool.dependecy_injector import DependecyInjector
from lib.interfaces import ArchtoolsClientLibBuilder


async def test_generate_client_lib(injector: DependecyInjector):
    client_lib_builder = ArchtoolsClientLibBuilder(injector=injector)
    generated_folder = client_lib_builder.generate_client_lib(dest_folder=Path.cwd() / "test_client_lib")
    generated_folder.create_all()
