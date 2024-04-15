from abc import abstractmethod
from archtool.layers.default_layer_interfaces import ABCController, ABCRepo

from lib.interfaces import RepoMixinsABC
from .dtos import (CreateServiceDTO,
                   RetieveServiceDTO,
                   UpdateServiceDTO,
                   DeleteServiceDTO,

                   CreateServiceCategoryDTO,
                   RetrieveServiceCategoryDTO,
                   UpdateServiceCategoryDTO,
                   DeleteServiceCategoryDTO)

from .datamappers import ServiceDM


# контроллеры
class ServicesControllerABC(ABCController):
    ...


class ServicesCategoryControllerABC(ABCController):
    ...


# репозитории
class ServiceCategoryRepoABC(ABCRepo):
    ...


class ServiceRepoABC(ABCRepo,
                     RepoMixinsABC[ServiceDM,
                                   CreateServiceDTO,
                                   RetieveServiceDTO,
                                   UpdateServiceDTO,
                                   DeleteServiceDTO
                                   ]):
    ...


class ServiceCategoryRepoABC(ABCRepo,
                     RepoMixinsABC[CreateServiceCategoryDTO,
                                   RetrieveServiceCategoryDTO,
                                   UpdateServiceCategoryDTO,
                                   DeleteServiceCategoryDTO]):
    ...
