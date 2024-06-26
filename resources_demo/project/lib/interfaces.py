from abc import abstractmethod, ABC
from contextlib import asynccontextmanager
import typing
from functools import wraps

from multimethod import multimethod
from sqlalchemy import select, update, delete, BinaryExpression, Selectable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pydantic import BaseModel, ConfigDict, validator
from archtool.layers.default_layer_interfaces import ABCController
from archtool.dependecy_injector import DependecyInjector

from exceptions import NotExist
from pydantic import TypeAdapter, Field


TT = typing.TypeVar("TT", bound=BaseModel)
CT = typing.TypeVar("CT", bound=BaseModel)
RT = typing.TypeVar("RT", bound="BaseSelection")
UT = typing.TypeVar("UT", bound=('FilterDTOABC'))
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

# для dto
class Blank(type):
    ...


T = typing.TypeVar("T")
DTOField = typing.Union[typing.Optional[T], Blank]
OneOrMultuple = typing.Union[T, list[T]]

from typing import Any, ClassVar, Optional, Type, Union


class PydanticWrapper(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def not_blank(self):
        return {key: value for key, value in vars(self).items() if value is not Blank}

class DTOBase(PydanticWrapper):
    selection: ClassVar[Optional['BaseSelection']] = None
    payload: ClassVar[Optional['DTOBase']] = None


class DMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PaginationInfo(BaseModel):
    get_all: bool = False
    default_chunk_size: int = 100
    chunk_size: typing.Optional[int]
    page_start: int = 0


class BaseSelection(PydanticWrapper):
    def __init__(self, **data):
        prepared_data = {}
        for key, value in data.items():
            splitted = key.split("__")
            name = splitted[0]
            if name not in prepared_data:
                prepared_data.update({name: []})
            field_expressions = prepared_data[name]
            new_expr = Expression(raw_expression=key, value=value)
            field_expressions.append(new_expr)
        super().__init__(**prepared_data)


class FilterDTOABC:
    payload: DTOBase
    selection: DTOBase


from enum import Enum


class NoSuchOperation(Exception):
    ...


class OperationTypes(Enum):
    gt = "__gt__"
    gte = "__gte__"
    lte = "__lte__"
    lt = "__lt__"
    eq = "__eq__"
    included = "in_"

def orm_all(expressions) -> BinaryExpression:
    expressions = list(expressions)
    final_expression = expressions.pop(0)
    while True:
        try:
            expr = expressions.pop(0)
            final_expression = final_expression & expr
        except IndexError:
            break
    return final_expression



def build_where_expr(selection: DTOBase,
                     selectable: DeclarativeBase) -> typing.Optional[BinaryExpression]:
    orm_expressions = []
    for expression, value in selection.not_blank.items():
        if isinstance(value, Expression):
            orm_expr = sql_from_expr(expr=value, selectable=selectable)
            orm_expressions.append(orm_expr)
        elif isinstance(value, list) and len(value) and isinstance(value[0], Expression):
            for expr in value:
                orm_expr = sql_from_expr(expr=expr, selectable=selectable)
                orm_expressions.append(orm_expr)
    return orm_all(orm_expressions)


def parse_query_string(string: str) -> tuple[str, OperationTypes]:
    # TODO: подрефачить
    if "__" not in string:
        name, expression = (string, "__eq__")
    else:
        name, expression = string.split("__")
        expression = f"__{expression}__" if expression != OperationTypes.included.value else "in_"

    expr_type = [el for el in OperationTypes if el.value == expression][0] 
    return name, expr_type    


def sql_from_expr(expr: 'Expression',
                  selectable: DeclarativeBase) -> BinaryExpression:
    readonly_column = getattr(selectable, expr.field_name)
    expression = getattr(readonly_column, expr.expression_type.value)(expr.value)
    return expression


ExprT = typing.TypeVar("ExprT")
from typing import ClassVar, Optional


class Expression(typing.Generic[ExprT], DTOBase):
    expression_type: OperationTypes
    field_name: str
    value: ExprT
    # TODO: сделать проброс oper_types в build_where_expr
    oper_types: ClassVar[OperationTypes] = OperationTypes

    def __init__(self, raw_expression: str, value: ExprT):
        field_name, expression_type = parse_query_string(raw_expression)
        value = value
        super().__init__(expression_type=expression_type,
                         value=value,
                         field_name=field_name)


Expressions = DTOField[OneOrMultuple[Expression[T]]]


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
    async def update(self, data: UT, session: typing.Optional[AsyncSession] = None) -> OneOrMultuple[TT]:
        ...

    @abstractmethod
    async def delete(self, data: DT, session: typing.Optional[AsyncSession] = None, commit: bool = False) -> int:
        ...

    @abstractmethod
    async def filter(self,
                     data: FilterDTOABC,
                     session: typing.Optional[AsyncSession] = None
                     ) -> TypeAdapter[list[TT]]:
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
        where_expression = build_where_expr(selection=data, selectable=self.model)
        query = select(self.model).where(where_expression).limit(1)
        async with self.get_or_create_session(session) as session:
            conn = await session.execute(query)
            res = conn.mappings().first()
            if res:
                result = res._data[0]
                return self.default_dm.model_validate(result)
            else:
                raise NotExist()

    async def update(self, data: UT, session: typing.Optional[AsyncSession] = None) -> OneOrMultuple[TT]:
        orm_expression: BinaryExpression = build_where_expr(selection=data.selection,
                                                            selectable=self.model)
        values = data.payload.not_blank
        query = update(self.model)\
                .where(orm_expression)\
                .values(**values)\
                .returning(self.model)
        async with self.get_or_create_session(session) as session:
            cursor = await session.execute(query)
            records = cursor.mappings().all()
            records = [list(e.values())[0] for e in records]
            result = self.serialize(records)
            return result

    def serialize(self, records) -> TT:
        records_quantity = len(records)
        if records_quantity == 1:
            serialized_result = self.default_dm.model_validate(records[1])
        elif records_quantity > 1:
            t = TypeAdapter(list[self.default_dm])
            serialized_result = t.validate_python(records)
        else:
            serialized_result = []
        return serialized_result

    async def delete(self, data: DT, session: typing.Optional[AsyncSession] = None, commit: bool = False) -> int:
        where_expr = build_where_expr(selection=data, selectable=self.model)
        query = delete(self.model).where(where_expr)
        async with self.get_or_create_session(session) as session:
            cursor = await session.execute(query)
            if commit:
                await session.commit()
            return cursor.rowcount


    @asynccontextmanager
    async def filter(self,
                     data: FilterDTOABC,
                     session: typing.Optional[AsyncSession] = None
                     ) -> typing.AsyncIterator[TypeAdapter[list[TT]]]:

        # TODO:
        where_expression: BinaryExpression = build_where_expr(data.selection_expr)
        query = select(self.model).where(data.filter_by_conditions)
        object_list_type = TypeAdapter[list[TT]]

        async with self.get_or_create_session(session) as session:
            conn = await session.execute(query)
            orm_result = conn.mappings().all()
            result = object_list_type.validate_python(orm_result)
            yield result



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


@multimethod
def resolve_controller_name(controller) -> str:
    ...


@resolve_controller_name.register
def _(controller: typing.Type[ABCController]) -> str:
    python_controller_name = controller.__name__
    return snake_case(python_controller_name.replace("Controller", ""))


@resolve_controller_name.register
def _(controller: ABCController) -> str:
    python_controller_name = controller.__class__.__name__
    return snake_case(python_controller_name.replace("Controller", ""))


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
    section_name = resolve_controller_name(controller)
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

PYTHON_TO_OPENAPI_TYPES_MAPPING = {
        str: "string",
        int: "integer",
        bool: "boolean",
        float: "float",
        # TODO: добавить форматирование для типов
        datetime.datetime: "string"
    }


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

def get_arg_type_of_method_by_index(cls, method_name: str, index: int):
    method = getattr(cls, method_name)
    type_hints = typing.get_type_hints(method)
    first_param_name = list(type_hints.keys())[index]
    return type_hints[first_param_name]


def wrap_method_as_endpoint(method: typing.Callable, method_type: 'RequestTypes'):
    # делаем инъекцию на основе аннотаций
    is_wrapped = False
    extra_payload_required = {}
    if hasattr(method, "__original__"):
        if "caller" in method.__annotations__:
            extra_payload_required.update({"caller": method.__annotations__["caller"]})
        wrapper = method 
        method = method.__original__
        is_wrapped = True
    
    function_to_call = wrapper if is_wrapped else method
    method_dto, method_dm = get_dto_and_dm(method=method)

    hardcoded_caller_data = dict(id=1,
                                 phone_number="+78005553555",
                                 username="chel",
                                 email="bebra@gmail.com",
                                 role_id=1)

    # TODO: хотелось бы как-то подрефакторить
    if method_type is RequestTypes.PATCH:
        async def wrapper(request: AIOHTTP_REQUEST) -> AIOHTTP_RESPONSE:
            if request.has_body:
                # как-то надо достать тип
                payload_class = method_dto.payload
                body = await request.json()
                payload = payload_class(**body)
                dto = method_dto(dict(**request.query, payload=payload))

                extra_payload = {}
                if "caller" in extra_payload_required:
                    caller_dto = extra_payload_required["caller"]
                    # TODO: где-то нужно пришить механизм аутендификации, сейчас хардкод
                    caller_instanse = caller_dto.model_validate(hardcoded_caller_data)
                    extra_payload.update(dict(caller=caller_instanse))
                result = await function_to_call(data=dto, **extra_payload)

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
            # TODO: самоповтор
            extra_payload = {}
            if "caller" in extra_payload_required:
                caller_dto: BaseModel = extra_payload_required["caller"]
                # TODO: где-то нужно пришить механизм аутендификации, сейчас хардкод
                caller_instanse = caller_dto.model_validate(hardcoded_caller_data)
                extra_payload.update(dict(caller=caller_instanse))
            result = await function_to_call(data=dto, **extra_payload)

            if type(result) is BaseModel:
                serialized_result = result.model_dumps()
            else:
                serialized_result = result
            return web.json_response(data=serialized_result,
                                     status=status_code,
                                     dumps=json_encoder)

    elif method_type in [RequestTypes.POST]:
        async def wrapper(request: AIOHTTP_REQUEST) -> AIOHTTP_RESPONSE:
            body = await request.json()
            dto = method_dto(dict(**request.body))

            extra_payload = {}
            if "caller" in extra_payload_required:
                caller_dto = extra_payload_required["caller"]
                # TODO: где-то нужно пришить механизм аутендификации, сейчас хардкод
                caller_instanse = caller_dto.model_validate(hardcoded_caller_data)
                extra_payload.update(dict(caller=caller_instanse))
            result = await function_to_call(data=dto, **extra_payload)

            if type(result) is BaseModel:
                serialized_result = result.model_dumps()
            else:
                serialized_result = result
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
                original_method = method
                method = reduce(lambda o, m: m(o), self.custom_middlewares, method)
                method.__original__ = original_method
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
    string = ("\n" + string).replace("\n", "\n" + (num_tabs * "  "))
    return string


import re

@dataclass
class Parameter:
    position: str
    name: str
    type: str
    required: bool


@dataclass
class OpenApiEndpoint:
    section_name: str
    endpoint: typing.Callable
    uri: str
    request_type: RequestTypes
    dto: DTOBase
    dm: DMBase
    parameters: list[Parameter]

    @property
    def path_parameters(self):
        pattern = r"\{([a-zA-Z]+).*\}"
        matches = re.findall(pattern, self.uri)
        return matches


from pydantic.fields import FieldInfo
from pydantic._internal._model_construction import ModelMetaclass


# немного хардкода с аннотированием возвращаемого значения
def get_dto_and_dm(method: typing.Callable) -> tuple[Type[DTOBase], Type[DMBase]]:
    original_class = find_method_origin(type(method.__self__), method.__name__)
    is_generic_method = original_class is ControllerMixins
    
    if not is_generic_method:
        method_dto: BaseModel = method.__annotations__["data"]
        annotations = method.__annotations__
        # dto_cls = [v for k, v in annotations.items() if k != 'return'][0]
        dm_cls = annotations.get('return', None)
        return method_dto, dm_cls
    else:
        # единственный найденый вариант
        # TODO: порнография, нужно оптимизировать
        generic_typevar = get_arg_type_of_method_by_index(type(method.__self__), method.__name__, 0)
        dto_index = original_class.__orig_bases__[0].__args__.index(generic_typevar)
        method_dto: BaseModel = method.__self__.__orig_bases__[1].__args__[dto_index]
        method_dm: BaseModel = method.__self__.__orig_bases__[1].__args__[0]
        return method_dto, method_dm


from jinja2 import Environment, select_autoescape, FileSystemLoader


class ArchtoolsOpenApiGenerator:
    DTO_BASE = BaseModel

    def __init__(self, injector: DependecyInjector, uri_prefix: str = "/api/"):
        self.injector = injector
        self.endpoints: list[OpenApiEndpoint] = []
        self.dtos = {}
        self.dms = {}
        self.uri_prefix = uri_prefix
        self._process_after = {}

        self.env = Environment(
            loader=FileSystemLoader(pathlib.Path(__file__).parent / "templates"),
            autoescape=select_autoescape()
        )

    def generate_openapi_model(self, model: Union[DTOBase, DMBase]) -> str:
        if issubclass(model, DMBase):
            fields = model.model_fields
        elif issubclass(model, DTOBase):
            if "payload" in model.model_fields:
                fields = model.model_fields['payload'].annotation.model_fields
            else:
                # временное условие
                fields = model.model_fields
        else:
            raise
        
        fields_rendered = ""
        required_fields_names = []
        for name, field in fields.items():
            rendered_field, is_field_required = self._render_object_property_field(name, field, model)
            fields_rendered += rendered_field + "\n"
            if is_field_required:
                required_fields_names.append(name) 

        required_rendered = "\n".join(" - " + e for e in required_fields_names)
        if required_rendered:
            required_rendered = tab_block("required:\n" + tab_block(required_rendered), num_tabs=3)
        properties = tab_block(f"properties:{tab_block(fields_rendered)}", num_tabs=3)
        rendered = f"type: object\n{required_rendered}\n{properties}"
        return rendered

    def _render_object_property_field(self, field_name: str, field: FieldInfo, model: BaseModel) -> tuple[str, bool]:
        # лютый ХАРДКОД
        property_field_template = self.env.get_template("property_field.jinja2")
        is_expression = "Expression" in str(field.annotation)
        is_ref = inspect.isclass(field.annotation) and issubclass(field.annotation, BaseModel)
        
        if is_ref:
            if field.annotation not in self.dtos:
                dto_code = self.generate_openapi_model(field.annotation)
                self.dtos.update({field.annotation: dto_code})
            return f"{field_name}:\n  $ref: '#/components/schemas/{field.annotation.__name__}'", True

        elif is_expression:
            raise Exception("expression can not be defined in payload")
            # если зааннотировано как экспрешены (либо как подклассы экспрешеннов)
            # парсим как множество различных полей.
            # вытаскиваем все операторы из связанных с экспрешенном
            # отображаем каждый возможный экспрешн
            # expr_annotation: Expression = field.annotation.__args__[0]
            # _type = expr_annotation.__args__[0]
            # openapi_type = PYTHON_TO_OPENAPI_TYPES_MAPPING[_type]
            # is_required = not (Blank in field.annotation.__args__)
            # rendered = ""
            # for available_oper in expr_annotation.oper_types:
                # field_rendered = property_field_template.render(type=openapi_type,
                                                                # field_name=f"{field_name}_{available_oper.value.replace('__', '')}")
                # rendered += "\n" + field_rendered
            # return rendered, is_required

        # если тип не DTOField[OneOrMultuple[...]] с Expression[T]
        else:
            field_annotation = field.annotation
            is_required = not (hasattr(field_annotation, "_name") and field_annotation._name == "Optional")
            _type = field_annotation.__args__[0] if hasattr(field_annotation, "__args__") else field_annotation
            if issubclass(type(_type), ModelMetaclass):
                # TODO:
                # self.get_ref_on_model(_type)
                return "", False
            else:
                rendered = f"{field_name}:\n  type: {PYTHON_TO_OPENAPI_TYPES_MAPPING[_type]}"
                return rendered, is_required


    def parse_parameters(self, dto: Union[DTOBase, BaseSelection]) -> list[Parameter]:
        results = []
        if issubclass(dto, DTOBase):
            if not 'selection' in dto.model_fields:
                return []
            else:
                fields = dto.model_fields['selection'].annotation.model_fields
        elif issubclass(dto, BaseSelection):
            fields = dto.model_fields
        else:
            raise

        for param_name, field in fields.items():
            is_expression = "Expression" in str(field.annotation)
            is_ref = inspect.isclass(field.annotation) and issubclass(field.annotation, BaseSelection)

            if is_ref:
                if field.annotation not in self.dtos:
                    results.extend(self.parse_parameters(field.annotation))

            elif is_expression:
                # если зааннотировано как экспрешены (либо как подклассы экспрешеннов)
                # парсим как множество различных полей.
                # вытаскиваем все операторы из связанных с экспрешенном
                # отображаем каждый возможный экспрешн
                expr_annotation: Expression = field.annotation.__args__[0]
                _type = expr_annotation.__args__[0]
                for available_oper in expr_annotation.oper_types:
                    new_param = Parameter(type=PYTHON_TO_OPENAPI_TYPES_MAPPING[_type],
                                          name=f"{param_name}_{available_oper.value.replace('__', '')}",
                                          required=False,
                                          position="query")
                    results.append(new_param)
            else:
                is_param_required = "NoneType" in str(field.annotation) # >.<
                param_type = field.annotation.__args__[0] if field.annotation.__args__ else field.annotation
                new_param = Parameter(name=param_name,
                                      position="path",
                                      type=PYTHON_TO_OPENAPI_TYPES_MAPPING[param_type],
                                      required=is_param_required)
                results.append(new_param)
        return results

    def generate_openapi(self, dest_file: pathlib.Path):
        # инициализация базовых папок
        # while True:
        #     if not dest_file.exists():
        #         dest_folder.mkdir()
        #         paths_folder = dest_folder / "paths"
        #         schemas_folder = dest_folder / "schemas"
        #         for folder in [paths_folder, schemas_folder]:
        #             folder.mkdir()
        #         break
        #     else:
        #         dest_folder.rmdir()

        # генерация
        controllers = get_api_controllers(self.injector)        
        paths = {}
        for controller in controllers:
            for method_name, method in get_controller_methods(controller).items():
                method_type = resolve_endpoint_method_type(method=method)
                is_method_detailed = resolve_endpoint_detailed(method, method_type=method_type)
                uri = resolve_uri(method=method, controller=controller, method_type=method_type)

                dto, dm = get_dto_and_dm(method)
                parameters = self.parse_parameters(dto)
                if dto not in self.dtos and not issubclass(dto, BaseSelection):
                    dto_code = self.generate_openapi_model(dto)
                    self.dtos.update({dto: dto_code})
                else:
                    dto = None
                if dm not in self.dtos:
                    dm_code = self.generate_openapi_model(dm)
                    self.dtos.update({dm: dm_code})


                openapi_endpoint = OpenApiEndpoint(section_name=resolve_controller_name(controller),
                                                   endpoint=method,
                                                   uri=uri,
                                                   request_type=method_type.value,
                                                   dto=dto,
                                                   dm=dm,
                                                   parameters=parameters)

                # self.endpoints.append(openapi_endpoint)
                if openapi_endpoint.uri in paths:
                    paths[openapi_endpoint.uri].append(openapi_endpoint)
                else:
                    paths.update({openapi_endpoint.uri: [openapi_endpoint]})

        specification_template = self.env.get_template("specification.jinja")
        rendered = specification_template.render(paths=paths,
                                                 components=self.dtos,
                                                 title="",
                                                 version="",
                                                 description="",
                                                 type=type)
        return rendered


class ArchtoolsGrpcGenerator:
    def generate_protobuff(self):
        ...


class ABCSender(ABC):

    @abstractmethod
    async def send(self, data: DTOBase) -> DMBase:
        raise NotImplementedError("Send method is not implemented!")


from aiohttp import ClientSession
import builtins

class AiohttpSender(ABCSender):
    client: ClientSession

    async def get_query_params(self, dto: DTOBase) -> Optional[dict[str, Any]]:
        result = {}

        return None if not result else result

    async def get_body(self, dto: DTOBase) -> Optional[dict[str, Any]]:
        result = {}

        return None if not result else result

    async def send(self,
                   data: DTOBase,
                   request_method: RequestTypes,
                   uri: str) -> DMBase:
        method = getattr(self.client, request_method.value)
        query_params = self.get_query_params(data)
        body = self.get_body(data)
        request_data = dict(params=query_params, body=body)

        async with method(uri, **request_data) as response:
            response


BUILTINS = list(vars(builtins).values())
from dataclasses import field

@dataclass
class ClientRepo:
    name: str
    methods: list['ClientRepoMethod'] = field(default_factory=list)

    @property
    def interface_name(self) -> str:
        return self.name + "ABC"


@dataclass
class ClientRepoMethod:
    name: str
    uri: str
    dto_name: str
    dm_name: str


@dataclass
class Folder:
    path: pathlib.Path
    files: list['File'] = field(default_factory=list)

    def create_all(self) -> None:
        try:
            self.path.rmdir()
        except Exception:
            ...
        self.path.mkdir()
        for _file in self.files:
            _file.create()


@dataclass
class File:
    parent: Folder
    name: pathlib.Path
    content: str

    @property
    def file_path(self) -> pathlib.Path:
        return self.parent.path / self.name

    def create(self) -> None:
        self.file_path.touch()
        self.file_path.write_text(self.content)


class ArchtoolsClientLibBuilder:
    def __init__(self, injector: DependecyInjector):
        self.injector = injector
        self.env = Environment(
            loader=FileSystemLoader(pathlib.Path(__file__).parent / "templates"),
            autoescape=select_autoescape())

    def generate_interface_from_component(self, component: ClientRepo):
        ...

    def generate_client_lib(self,
                            dest_folder: pathlib.Path,
                            sender: Type[ABCSender] = AiohttpSender) -> Folder:

        dtos: dict[DTOBase, Optional[str]] = {}
        dto_dependencies: set[str] = set()

        datamappers: dict[DMBase, Optional[str]] = {}
        dm_dependencies: set[str] = set()

        repositories: ClientRepo = []
        repo_interfaces = []

        for controller in get_api_controllers(self.injector):
            repository_name = type(controller).__name__.replace("Controller", "Repo")
            repo_methods = []
            for method_name, method in get_controller_methods(controller).items():
                method_type = resolve_endpoint_method_type(method=method)
                uri = resolve_uri(method=method, controller=controller, method_type=method_type)

                dto, dm = get_dto_and_dm(method)
                if not dto in dtos:
                    dto_code = inspect.getsource(dto)
                    dtos.update({dto: dto_code})
                    deps = self.get_object_dependencies(dto)
                    dto_dependencies = dto_dependencies.union(deps)

                if not dm in datamappers:
                    dm_code = inspect.getsource(dm)
                    datamappers.update({dm: dm_code})
                    deps = self.get_object_dependencies(dm)
                    dm_dependencies = dm_dependencies.union(deps)

                new_method = ClientRepoMethod(name=method_name,
                                              uri=uri,
                                              dm_name=dm.__name__,
                                              dto_name=dto.__name__)
                repo_methods.append(new_method)

            client_repo = ClientRepo(name=repository_name,
                                     methods=repo_methods)
            repo_interface = self.generate_interface_from_component(client_repo)
            repo_interfaces.append(repo_interface)
            repositories.append(client_repo)
        
        dto_file_content = ""
        dm_file_content = ""
        repos_file_content = ""
        interfaces_file_content = ""

        dto_template = self.env.get_template("client_lib/dtos.jinja")
        repos_template = self.env.get_template("client_lib/repos.jinja")
        # TODO:
        # self.env.get_template("client_lib/interfaces.jinja")

        dto_file_content = dto_template.render(dependencies=dto_dependencies,
                                               dtos=dtos)

        dm_file_content = dto_template.render(dependencies=dm_dependencies,
                                              dtos=datamappers)

        repos_file_content = repos_template.render(repo_deps=[],
                                                   repos=repositories)

        root_folder = Folder(path=dest_folder)
        root_folder.files = [File(parent=root_folder, name="interfaces.py", content=interfaces_file_content),
                             File(parent=root_folder, name="repos.py", content=repos_file_content),
                             File(parent=root_folder, name="dms.py", content=dm_file_content),
                             File(parent=root_folder, name="dtos.py", content=dto_file_content)]
        return root_folder


    def get_object_dependencies(self, obj: Union[DTOBase, DMBase]) -> set[str]:
        object_deps = set()
        for name, annotation in obj.__annotations__.items():
            if not type(annotation) in BUILTINS:
                dep_module = annotation.__module__
                dep_name = annotation.__name__
                dep_import_string = f"from {dep_module} import {dep_name}"    # для typing.Option неправильно формируется строка
                object_deps.add(dep_import_string)                            # так же мы не смотрим на классы, от которых наследуемся, хотя надо !
        return object_deps
