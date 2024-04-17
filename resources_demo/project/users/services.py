from project.lib.interfaces import ServiceMixins
from .datamappers import InnerUserDM
from .dtos import (CreateInnerUserDTO,
                   RetrieveInnerUserDTO,
                   UpdateInnerUserDTO,
                   DeleteInnerUserDTO)
from .interfaces import UserServiceABC, UserRepoABC


class UserService(UserServiceABC,
                  ServiceMixins[
                    InnerUserDM,
                    CreateInnerUserDTO,
                    RetrieveInnerUserDTO,
                    UpdateInnerUserDTO,
                    DeleteInnerUserDTO]):

    default_repo: UserRepoABC
