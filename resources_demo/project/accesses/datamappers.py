from typing import Optional
from lib import DMBase


class PolicyDM(DMBase):
    id: int
    policy_on: str
    policy: Optional[dict]
    conditions: list[str]