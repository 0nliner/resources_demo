from dataclasses import dataclass
from pydantic import BaseModel

from core import CallerDTO


@dataclass
class AccessContext:
    dto: BaseModel
    caller: CallerDTO
