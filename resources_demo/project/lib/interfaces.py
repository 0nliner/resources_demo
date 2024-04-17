from abc import abstractmethod, ABC
from contextlib import asynccontextmanager
import typing
from functools import wraps

from sqlalchemy import select, update, delete, BinaryExpression, Selectable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pydantic import BaseModel
from archtool.layers.default_layer_interfaces import ABCController
from archtool.dependecy_injector import DependecyInjector

from exceptions import NotExist


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
            res = conn.mappings().first()
            if res:
                result = res._data[0]
                return self.default_dm.model_validate(result)
            else:
                raise NotExist()
            

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



from archtool.layers.default_layer_interfaces import ABCRepo, ABCService


class ServiceMixinsABC(ABC, typing.Generic[TT, CT, RT, UT, DT]):
    @abstractmethod
    async def create(self, data: CT) -> TT:
        ...

    @abstractmethod
    async def retrieve(self, data: RT) -> TT:
        ...

    @abstractmethod
    async def update(self, data: UT) -> TT:
        ...

    @abstractmethod
    async def delete(self, data: DT) -> TT:
        ...


class ServiceMixins(ServiceMixinsABC[TT, CT, RT, UT, DT]):
    default_repo: ABCRepo

    async def create(self, data: CT) -> TT:
        new_object = await self.default_repo.create(data)
        return new_object

    async def retrieve(self, data: RT) -> TT:
        result = await self.default_repo.retrieve(data)
        return result

    async def update(self, data: UT) -> TT:
        result = await self.default_repo.update(data)
        return result

    async def delete(self, data: DT) -> TT:
        # что делаем со связанными данными ?
        result = await self.default_repo.delete(data)
        return result


class ControllerMixinsABC(ABC, typing.Generic[TT, CT, RT, UT, DT]):
    @abstractmethod
    async def create(self, data: CT) -> TT:
        ...

    @abstractmethod
    async def retrieve(self, data: RT) -> TT:
        ...

    @abstractmethod
    async def update(self, data: UT) -> TT:
        ...

    @abstractmethod
    async def delete(self, data: DT) -> TT:
        ...


class ControllerMixins(ControllerMixinsABC[TT, CT, RT, UT, DT]):
    default_service: ABCService

    async def create(self, data: CT) -> TT:
        new_object = await self.default_service.create(data)
        return new_object

    async def retrieve(self, data: RT) -> TT:
        result = await self.default_service.retrieve(data)
        return result

    async def update(self, data: UT) -> TT:
        result = await self.default_service.update(data)
        return result

    async def delete(self, data: DT) -> TT:
        # что делаем со связанными данными ?
        result = await self.default_service.delete(data)
        return result


# ----------------------------------------------------------------------------------
# class APIController(ABCController):
#     @abstractmethod
#     @classmethod
#     def collect_endpoints(cls) -> dict[str, typing.Callable]:
#         ...


# class BaseAPIController(APIController):
#     @classmethod
#     def collect_methods(cls)


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

import inspect
from archtool.layers.default_layer_interfaces import ABCController

def get_api_controllers(injector: DependecyInjector) -> list[ABCController]:
    result = []
    for value in injector._dependencies.values():
        if isinstance(value, ABCController):
            result.append(value)  
    return result


def get_controller_methods(controller: ABCController) -> dict[str, typing.Callable]:
    methods = {}
    for key in dir(controller):
        value = getattr(controller, key)
        # TODO: добавить проверку того, что метод не в классе BaseAPIController
        if callable(value) and not key.startswith("__"):
            methods.update({key: value})
    return methods

def resolve_controller_name(name: str) -> str:
    return snake_case(name.replace("Controller", ""))


def resolve_endpoint_method_type(method: typing.Callable) -> 'RequestTypes':
    # TODO: прототип, требуется более "смышлённый" механизм
    operation_name = method.__name__
    if "create" in operation_name:
        return RequestTypes.POST
    elif "update" in operation_name:
        return RequestTypes.PATCH
    elif ("retrieve" in operation_name) or ("get" in operation_name) or ("list" in operation_name):
        return RequestTypes.GET
    elif "delete" in operation_name:
        return RequestTypes.DELETE
    else:
        return RequestTypes.UNDEFINED


def resolve_endpoint_detailed(method: typing.Callable, method_type: 'RequestTypes') -> bool:
    is_detailed = False
    if method_type in (RequestTypes.GET, RequestTypes.DELETE):
        is_detailed = True
    return is_detailed

def resolve_uri(method: typing.Callable,
                controller: ABCController,
                method_type: 'RequestTypes') -> str:
    # TODO: тут тоже нужно пошаманить
    is_detailed = resolve_endpoint_detailed(method=method, method_type=method_type)
    section_name = resolve_controller_name(controller.__class__.__name__)
    operation_name = method.__name__
    uri = f"{section_name}"
    uri = f"{uri}/{operation_name}" if method_type is RequestTypes.UNDEFINED else uri
    uri = uri + r"/{id:\d+}" if is_detailed else uri
    return uri


def endpoints_iterator(controllers: list[ABCController]):
    ...    

import json
import datetime
import enum 
from uuid import UUID
from aiohttp import web_app, web
from aiohttp.web_request import Request as AIOHTTP_REQUEST
from aiohttp.web_response import Response as AIOHTTP_RESPONSE


def json_encoder(*args, **kwargs):
    def encoder(obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        if isinstance(obj, int) or isinstance(obj, UUID) or isinstance(obj, enum.Enum):
            return str(obj)
    return json.dumps(default=encoder, *args, **kwargs)


def find_method_origin(cls, method_name):
    """Определяет класс, в котором был определен метод с именем method_name."""
    for base_class in inspect.getmro(cls):
        if method_name in base_class.__dict__:
            return base_class
    return None

def get_first_arg_type_of_method(cls, method_name: str):
    method = getattr(cls, method_name)
    type_hints = typing.get_type_hints(method)
    first_param_name = list(type_hints.keys())[0]
    return type_hints[first_param_name]


def wrap_method_as_endpoint(method: typing.Callable, method_type: 'RequestTypes'):
    # чернуха
    original_class = find_method_origin(type(method.__self__), method.__name__)
    is_generic_method = original_class is ControllerMixins
    
    if not is_generic_method:
        method_dto: BaseModel = method.__annotations__["data"]
    else:
        # единственный найденый вариант
        # TODO: порнография, нужно оптимизировать
        generic_typevar = get_first_arg_type_of_method(type(method.__self__), method.__name__)
        dto_index = original_class.__orig_bases__[0].__args__.index(generic_typevar)
        method_dto: BaseModel = method.__self__.__orig_bases__[1].__args__[dto_index]

    # менее чернуха
    if method_type is RequestTypes.PATCH:
        async def wrapper(request: AIOHTTP_REQUEST) -> AIOHTTP_RESPONSE:
            if request.has_body:
                # как-то надо достать тип
                payload_class = method_dto.payload
                body = await request.json()
                payload = payload_class(**body)
                dto = method_dto(dict(**request.query, payload=payload))
                result = await method(dto)
                if type(result) is BaseModel:
                    serialized_result = result.model_dumps()
                # TODO: отправка ответа
                return web.json_response(data=serialized_result,
                                         status=200,
                                         dumps=json_encoder)
    elif method_type in [RequestTypes.GET, RequestTypes.DELETE]:
        status_code = {RequestTypes.GET: "200", RequestTypes.DELETE: "204"}[method_type]
        
        async def wrapper(request: AIOHTTP_REQUEST) -> AIOHTTP_RESPONSE:
            raw_data = request.query
            dto = method_dto.model_validate({**request.query, **dict(request.match_info)})
            result = await method(dto)
            if type(result) is BaseModel:
                serialized_result = result.model_dumps()
            else:
                serialized_result = result
            return web.json_response(data=status_code,
                                     status=200,
                                     dumps=json_encoder)
    elif method_type in [RequestTypes.POST]:
        async def wrapper(request: AIOHTTP_REQUEST) -> AIOHTTP_RESPONSE:
            body = await request.json()
            dto = method_dto(dict(**request.body))
            result = await method(dto)
            if type(result) is BaseModel:
                serialized_result = result.model_dumps()
            # TODO: отправка ответа
            return web.json_response(data=serialized_result,
                                     status=200,
                                     dumps=json_encoder)
    else:
        raise
    return wrapper


from functools import reduce


class ArchtoolsAPIGenerator:
    def __init__(self, injector: DependecyInjector, uri_prefix: str = "/api/", custom_middlewares=[]):
        self.injector = injector
        self.uri_prefix = uri_prefix
        self.custom_middlewares = custom_middlewares

    def aiohttp_app(self, loop) -> web_app.Application:
        http_app = web_app.Application(loop=loop)
        controllers = get_api_controllers(injector=self.injector)
        for controller in controllers:
            for method_name, method in get_controller_methods(controller).items():
                method_type = resolve_endpoint_method_type(method=method)
                uri = self.uri_prefix + resolve_uri(method=method,
                                                    controller=controller,
                                                    method_type=method_type)
                router_method = getattr(http_app.router, f"add_{method_type.value}")
                # оборачиваем метод в мидлвары
                # TODO: норм работает ?
                result = reduce(lambda o, m: m(o), self.custom_middlewares, method)
                method = method
                # оборачиваем в эндпоинт и регистрируем роут
                endpoint = wrap_method_as_endpoint(method, method_type=method_type)
                router_method(uri, endpoint)
        return http_app


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
from archtool.utils import string_to_snake_case as snake_case


class RequestTypes(Enum):
    POST = "POST".lower()
    GET = "GET".lower()
    PATCH = "PATCH".lower()
    DELETE = "DELETE".lower()
    OPTIONS = "OPTIONS".lower()
    UNDEFINED = "undefined"


def tab_block(string: str, num_tabs=1):
    string = ("\n" + string).replace("\n", "\n" + (num_tabs * "\t"))
    return string

@dataclass
class OpenApiEndpoint:
    endpoint: typing.Callable
    uri: str
    request_type: RequestTypes
    dto: BaseModel
    dm: BaseModel

from pydantic.fields import FieldInfo
from pydantic._internal._model_construction import ModelMetaclass

# немного хардкода с аннотированием возвращаемого значения
def get_dto_and_dm(method: typing.Callable) -> tuple[BaseModel, BaseModel]:
    annotations = method.__annotations__
    dto_cls = [v for k, v in annotations.items() if k != 'return'][0]
    dm_cls = annotations.get('return', None)
    return dto_cls, dm_cls


class ArchtoolsOpenApiGenerator:
    DTO_BASE = BaseModel
    TYPES_MAPPING = {
        str: "string",
        int: "integer",
        bool: "boolean",
        float: "float"
    }

    def __init__(self, injector: DependecyInjector, uri_prefix: str = "/api/"):
        self.injector = injector
        self.endpoints: list[OpenApiEndpoint] = []
        self.dtos = {}
        self.dms = {}
        self.uri_prefix = uri_prefix
        self._process_after = {}

    def generate_openapi_model(self, model: BaseModel) -> str:
        fields = model.model_fields
        fields_rendered = ""
        required_fields_names = []
        for name, field in fields.items():
            rendered_field, is_field_required = self._render_object_property_field(name, field, model)
            fields_rendered += rendered_field + "\n"
            if is_field_required:
                required_fields_names.append(name) 

        required_rendered = "".join(" - " + e for e in required_fields_names)
        if required_rendered:
            required_rendered = "required:\n" + required_rendered
        rendered = f"type: object\n{required_rendered}\nproperties:{tab_block(fields_rendered)}"
        return rendered

    def _render_object_property_field(self, field_name: str, field: FieldInfo, model: BaseModel) -> tuple[str, bool]:
        field_annotation = model.__annotations__[field_name]
        is_required = not (hasattr(field_annotation, "_name") and field_annotation._name == "Optional")
        _type = field_annotation.__args__[0] if hasattr(field_annotation, "__args__") else field_annotation
        if issubclass(type(_type), ModelMetaclass):
            # TODO:
            # self.get_ref_on_model(_type)
            return "", False
        else:
            rendered = f"{field_name}:\n\ttype: {self.TYPES_MAPPING[_type]}"
            return rendered, is_required

    def get_ref_on_model(self, model: BaseModel):
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
            controller_name = type(controller).__name__
            new_controller_name = resolve_controller_name(controller_name)
            sections_with_methods = {"detailed": [], new_controller_name: []}
            for method_name, method in get_controller_methods(controller).items():
                operation_id = method_name
                method_type = resolve_endpoint_method_type(method=method)
                is_method_detailed = resolve_endpoint_detailed(method, method_type=method_type)
                uri = resolve_uri(method=method, controller=controller, method_type=method_type)

                dto, dm = get_dto_and_dm(method)
                if dto not in self.dtos:
                    dto_code = self.generate_openapi_model(dto)
                    self.dtos.update({dto: dto_code})

                openapi_endpoint = OpenApiEndpoint(endpoint=method,
                                                   uri=uri,
                                                   request_type=method_type.value,
                                                   dto=dto,
                                                   dm=dm)
                case_1 = not uri.endswith(new_controller_name)
                case_2 = not uri.endswith('{id:\d+}')
                is_special_name = uri.endswith(new_controller_name) and uri.endswith('{id:\d+}')
                if is_special_name and not is_method_detailed:
                    sections_with_methods[new_controller_name].append(openapi_endpoint)
                elif is_method_detailed and not is_special_name:
                    sections_with_methods["detailed"].append(openapi_endpoint)
                else:
                    sections_with_methods.update({operation_id: openapi_endpoint})
                self.endpoints.append(openapi_endpoint)
            # создаём папку для контроллера
            controller_paths_folder = paths_folder / new_controller_name
            controller_paths_folder.mkdir()
            # нужно создать файлы под хранение каждого типа метода 
            # controller_paths_folder / controller_name




        controllers = get_api_controllers(injector=self.injector)
        for controller in controllers:
            for method_name, method in get_controller_methods(controller).items():
                method_type = resolve_endpoint_method_type(method=method)
                uri = self.uri_prefix + resolve_uri(method=method,
                                                    controller=controller,
                                                    method_type=method_type)
                router_method = getattr(http_app.router, f"add_{method_type.value}")


class ArchtoolsGrpcGenerator:
    def generate_protobuff(self):
        ...


class ArchtoolsClientLibGenerator:
    ...
