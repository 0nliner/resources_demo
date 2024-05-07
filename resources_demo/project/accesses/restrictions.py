from abc import ABC
from enum import Enum
from typing import Callable, Generic, TypeVar
from sqlalchemy import select
from core import Denormalized, CallerDTO


T = TypeVar("T")


def users_from_one_product(caller: CallerDTO) -> bool:
    select().where()


def owner_objects_restriction(model: Denormalized):
    # TODO: сделать проброс полей к которым происходит обращение
    owner_key = "owner"
    query = select(model.id).where((model.extra.op("->")(owner_key) != None) and (model.extra[owner_key]))
    return query


def is_from_one_space(model, caller_id):
    ...

