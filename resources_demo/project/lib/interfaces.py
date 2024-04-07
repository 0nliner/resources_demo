from abc import abstractmethod, ABC
from contextlib import asynccontextmanager
import typing
from functools import wraps

from sqlalchemy import select, update, delete, BinaryExpression, Selectable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pydantic import BaseModel
from archtool.layers.default_layer_interfaces import ABCController
from archtool.dependency_injector import DependecyInjector


TT = typing.TypeVar("TT", bound=BaseModel)
CT = typing.TypeVar("CT", bound=BaseModel)
RT = typing.TypeVar("RT", bound=BaseModel)
UT = typing.TypeVar("UT", bound=BaseModel)
DT = typing.TypeVar("DT", bound=BaseModel)

DTO_T = typing.Union[CT, RT, UT, DT]
# DM_T = typing.Union[TT, None]
DM_T = TT


G_DM_T = typing.TypeVar("G_DM_T", bound=DM_T)


# class get_or_create_session(typing.Generic[DM_T]):
#     def __init__(self, method: typing.Callable):
#         self.method = method

#     # @classmethod
#     def __call__(self, data: DTO_T, session: typing.Optional[AsyncSession] = None) -> DM_T:
#         async def wrapper():
#             if not session:
#                 async with sessionmaker.begin() as session:
#                     result = await self.method(self, data, session)
#                     return result
#             else:
#                 result = await self.method(self, data=data, session=session)
#                 return result
#         return wrapper

P = typing.ParamSpec('P')
T = typing.TypeVar("T")


class FilterDTOABC(ABC):
    ...


def build_where_expr(data: FilterDTOABC, selectable: Selectable) -> typing.Optional[BinaryExpression]:
    # пока простой пример
    expression: typing.Optional[BinaryExpression] = None
    for key, val in vars(data).items():
        attr = getattr(selectable, key)
        expression = expression and (attr == val) if expression else (attr == val)
    return expression


class RepoMixinsABC(ABC, typing.Generic[TT, CT, RT, UT, DT]):
    @abstractmethod
    async def create(self,
                     data: RT,
                     session: typing.Optional[AsyncSession] = None,
                     commit=False) -> TT:
        ...

    @abstractmethod
    async def retrieve(self, data: RT, session: typing.Optional[AsyncSession] = None) -> TT:
        ...

    @abstractmethod
    async def update(self, data: UT, session: typing.Optional[AsyncSession] = None) -> TT:
        ...

    @abstractmethod
    async def delete(self, data: DT, session: typing.Optional[AsyncSession] = None) -> None:
        ...


class RepoMixins(RepoMixinsABC[TT, CT, RT, UT, DT]):
    model: DeclarativeBase
    session_maker: sessionmaker

    @property
    def default_dm(self) -> TT:
        return self.dtos[0]

    @property
    def create_dto(self) -> TT:
        return self.dtos[1]

    @property
    def retrieve_dto(self) -> TT:
        return self.dtos[2]

    @property
    def update_dto(self) -> TT:
        return self.dtos[3]

    @property
    def delete_dto(self) -> TT:
        return self.dtos[4]

    @property
    def dtos(self):
        return self.__orig_bases__[1].__args__

    @asynccontextmanager
    async def get_or_create_session(self, session: typing.Optional[AsyncSession]) -> typing.AsyncIterator[AsyncSession]:
        if not session:
            session = self.session_maker()
            yield session
            await session.close()
        else:
            yield session


    async def create(self,
                     data: CT,
                     session: typing.Optional[AsyncSession] = None,
                     commit=False) -> TT:
        async with self.get_or_create_session(session) as session:
            new_object = self.model(**dict(data))
            session.add(new_object)
            if commit:
                await session.commit()
            return self.default_dm.model_validate(new_object)

    async def retrieve(self, data: RT, session: typing.Optional[AsyncSession] = None) -> TT:
        where_expression = build_where_expr(data, self.model)
        query = select(self.model).where(where_expression).limit(1)
        async with self.get_or_create_session(session) as session:
            conn = await session.execute(query)
            res = conn.mappings().first()._data[0]
            return self.default_dm.model_validate(res)

    async def update(self, data: UT, session: typing.Optional[AsyncSession] = None) -> TT:
        orm_expression: BinaryExpression = build_where_expr(data)
        values = {}
        query = update(self.model)\
                .where(orm_expression)\
                .values(**values)\
                .returning(self.model)
        async with self.get_or_create_session(session) as session:
            records = await session.execute(query)
            session.add_all(records)
            return records

    async def delete(self, data: DT, session: typing.Optional[AsyncSession] = None) -> DT:
        where_expr = build_where_expr(data)
        query = delete(self.model).where(where_expr)
        async with self.get_or_create_session(session) as session:
            await session.execute(query)



"""
Пример использования миксин

from users.datamappers import SSOUserDM

class UsersRepo(RepoMixins[SSOUserDM]):
    ...

async def test():
    ur = UsersRepo()
    result = await ur.get(data=1)
"""


class APIController(ABCController):
    @abstractmethod
    @classmethod
    def collect_endpoints(cls) -> dict[str, typing.Callable]:
        ...


class BaseAPIController(APIController):
    @classmethod
    def collect_methods(cls) -> dict[str, typing.Callable]:
        methods = {}
        for key, value in vars(cls):
            # TODO: добавить проверку того, что метод не в классе BaseAPIController
            if callable(value):
                methods.update({key, value})
        return methods
    

import pathlib
from enum import Enum, auto


class SpecificationExtensions(Enum):
    OPENAPI = auto()
    GRPC = auto()


class SpecificationBuilderABC(ABC):
    @abstractmethod
    def read(spec_path: pathlib.Path):
        spec_path.read_text()


class GrpcBuilder(SpecificationBuilderABC):
    ...

class OpenAPIBuilder(SpecificationBuilderABC):
    ...


def get_api_controllers(injector: DependecyInjector) -> list[APIController]:
    result = []
    for value in injector._dependencies.values():
        if issubclass(value, BaseAPIController):
            result.append(value)  
    return result


class ArchtoolsAPIMapper:
    EXTENSIONS_MAPPING = {".yaml": SpecificationExtensions.OPENAPI,
                          ".proto": SpecificationExtensions.GRPC}
    BUILDERS_MAPPING = {SpecificationExtensions.OPENAPI: OpenAPIBuilder,
                        SpecificationExtensions.GRPC: GrpcBuilder}
 
    def __init__(self, injector: DependecyInjector, specifications: list[pathlib.Path]):
        self.injector = injector
        self.specifications = specifications

    def map_controllers_on_specificaion(self):
        controllers = get_api_controllers()
        for spec_path in self.specifications:
            specification_type = self.EXTENSIONS_MAPPING[spec_path.suffix]
            builder = self.BUILDERS_MAPPING[specification_type]
            builder

    def methods_from_api_controllers(self):
        '''
        генерирует api контроллеры из контроллеров
        '''
        ...

    def generate_api_controllers_from_repos(self):
        '''
        генерирует api контроллеры из репозиториев
        '''
        ...


from pydantic import BaseModel
from dataclasses import dataclass
from archtools.utils import snake_case


class RequestTypes(Enum):
    POST = auto()
    GET = auto()
    PATCH = auto()
    DELETE = auto()
    OPTIONS = auto()


@dataclass
class OpenApiEndpoint:
    endpoint: typing.Callable
    request_type: RequestTypes
    dto: BaseModel
    dm: BaseModel


class ArchtoolsOpenApiGenerator:
    DTO_BASE = BaseModel

    def __init__(self, injector: DependecyInjector):
        self.injector = injector
        self.endpoints: list[OpenApiEndpoint] = []
        self.dtos = {}
        self.dms = {}

    def resolve_controller_name(self, name: str) -> str:
        return snake_case(name.replace("Controller"))

    def resolve_endpoint_method_type(self) -> RequestTypes:
        ...
    
    def resolve_endpoint_detailed(self) -> bool:
        ...

    # немного хардкода с аннотированием возвращаемого значения
    def get_dto_and_dm(self, method: typing.Callable) -> tuple[BaseModel, BaseModel]:
        annotations = method.__annotations__
        dto_cls = [v for k, v in annotations.items() if k != 'return']
        dm_cls = annotations.get('return', None)
        return dto_cls, dm_cls

    def generate_openapi_model(self, model: BaseModel):
        ...

    def generate_openapi(self, dest_folder: pathlib.Path):
        # инициализация базовых папок
        while True:
            if not dest_folder.exists():
                dest_folder.mkdir()
                paths_folder = dest_folder / "paths"
                schemas_folder = dest_folder / "schemas"
                for folder in [paths_folder, schemas_folder]:
                    folder.mkdir()
                break
            else:
                dest_folder.rmdir()

        # генерация
        controllers = get_api_controllers(self.injector)        
        for controller in controllers:
            for method_name, method in controller.collect_methods():
                operation_id = method_name
                is_method_detailed = self.resolve_endpoint_detailed(method)
                endpoint_method_type = self.resolve_endpoint_method_type(method)
                dto, dm = self.get_dto_and_dm(method)
                if dto not in self.dtos:
                    dto_code = self.generate_openapi_model(dto)
                    self.dtos.update({dto: dto_code})

                openapi_endpoint = OpenApiEndpoint(endpoint=method,
                                                   dto=dto,
                                                   dm=dm)
                self.endpoints.append(openapi_endpoint)
            
            # создаём папку для контроллера
            controller_name = controller.__name__
            new_controller_name = self.resolve_controller_name(controller_name)
            controller_paths_folder = paths_folder / new_controller_name



class ArchtoolsGrpcGenerator:
    def generate_protobuff(self):
        ...
