from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import TypeAdapter

from .interfaces import PolicyRepoABC
from .datamappers import *
from .dtos import *
from .models import Policy

from lib.interfaces import RepoMixins


class PolicyRepo(PolicyRepoABC,
                 RepoMixins[
                     PolicyDM,
                     CreatePolicyDTO,
                     RetrievePolicyDTO,
                     UpdatePolicyDTO,
                     DeletePolicyDTO]):

    model = Policy

    async def get_polices_by_controller_name(self, controller_name: str, session: Optional[AsyncSession] = None) -> list[PolicyDM]:
        query = select(Policy).where(Policy.policy_on == controller_name)
        async with self.get_or_create_session(session) as session:
            conn = await session.execute(query)
            orm_result = conn.mappings().all()
            # TODO: можно сделать автоматическую сериализацию
            # нужно смотреть на базовый класс возвращаемого значения, если в __mro__ есть DMBase - сериализуем автоматически
            # для этого требуется механизм мидлваров между слоями. Фича для archtool
            t = TypeAdapter(list[PolicyDM])
            serialized_result = t.validate_python(orm_result)
            return serialized_result
