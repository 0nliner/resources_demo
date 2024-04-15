from abc import abstractmethod
from archtool.layers.default_layer_interfaces import ABCController, ABCService, ABCRepo

from lib.interfaces import RepoMixinsABC, ServiceMixinsABC, ControllerMixinsABC

from .dtos import *
from .datamappers import *


# контроллеры
class PropertyControllerABC(ABCController,
                            ControllerMixinsABC[
                                PropertyDM,
                                CreatePropertyDTO,
                                RetrievePropertyDTO,
                                UpdatePropertyDTO,
                                DeletePropertyDTO]):
    ...


class ManufacturerControllerABC(ABCController,
                                ControllerMixinsABC[
                                    ManufacturerDM,
                                    CreateManufacturerDTO,
                                    RetrieveManufacturerDTO,
                                    UpdateManufacturerDTO,
                                    DeleteManufacturerDTO]):
    ...

class DeviceTypeControllerABC(ABCController,
                              ControllerMixinsABC[
                                DeviceTypeDM,
                                CreateDeviceTypeDTO,
                                RetrieveDeviceTypeDTO,
                                UpdateDeviceTypeDTO,
                                DeleteDeviceTypeDTO]):
    ...

class DeviceModelControllerABC(ABCController,
                               ControllerMixinsABC[
                                DeviceModelDM,
                                CreateDeviceModelDTO,
                                RetrieveDeviceModelDTO,
                                UpdateDeviceModelDTO,
                                DeleteDeviceModelDTO]):
    ...


class DeviceControllerABC(ABCController,
                          ControllerMixinsABC[
                            DeviceDM,
                            CreateDeviceDTO,
                            RetrieveDeviceDTO,
                            UpdateDeviceDTO,
                            DeleteDeviceDTO]):
    ...



# сервисы
class PropertyServiceABC(ABCService,
                             ServiceMixinsABC[
                               PropertyDM,
                               CreatePropertyDTO,
                               RetrievePropertyDTO,
                               UpdatePropertyDTO,
                               DeletePropertyDTO
                             ]):
    ...


class ManufacturerServiceABC(ABCService,
                             ServiceMixinsABC[
                               ManufacturerDM,
                               CreateManufacturerDTO,
                               RetrieveManufacturerDTO,
                               UpdateManufacturerDTO,
                               DeleteManufacturerDTO
                             ]):
    ...

class DeviceTypeServiceABC(ABCService,
                             ServiceMixinsABC[
                               DeviceTypeDM,
                               CreateDeviceTypeDTO,
                               RetrieveDeviceTypeDTO,
                               UpdateDeviceTypeDTO,
                               DeleteDeviceTypeDTO
                             ]):
    ...

class DeviceModelServiceABC(ABCService,
                             ServiceMixinsABC[
                               DeviceModelDM,
                               CreateDeviceModelDTO,
                               RetrieveDeviceModelDTO,
                               UpdateDeviceModelDTO,
                               DeleteDeviceModelDTO
                             ]):
    ...


class DeviceServiceABC(ABCService,
                       ServiceMixinsABC[
                           DeviceDM,
                           CreateDeviceDTO,
                           RetrieveDeviceDTO,
                           UpdateDeviceDTO,
                           DeleteDeviceDTO
                           ]):
    ...

# репозитории
class ManufacturerRepoABC(ABCRepo,
                          RepoMixinsABC[
                            ManufacturerDM,
                            CreateManufacturerDTO,
                            RetrieveManufacturerDTO,
                            UpdateManufacturerDTO,
                            DeleteManufacturerDTO
                          ]):
    ...

class DeviceTypeRepoABC(ABCRepo,
                          RepoMixinsABC[
                            DeviceTypeDM,
                            CreateDeviceTypeDTO,
                            RetrieveDeviceTypeDTO,
                            UpdateDeviceTypeDTO,
                            DeleteDeviceTypeDTO
                          ]):
    ...

class DeviceModelRepoABC(ABCRepo,
                          RepoMixinsABC[
                            DeviceModelDM,
                            CreateDeviceModelDTO,
                            RetrieveDeviceModelDTO,
                            UpdateDeviceModelDTO,
                            DeleteDeviceModelDTO
                          ]):
    ...


class DeviceRepoABC(ABCRepo,
                      RepoMixinsABC[DeviceDM,
                                    CreateDeviceDTO,
                                    RetrieveDeviceDTO,
                                    UpdateDeviceDTO,
                                    DeleteDeviceDTO]):
    ...


class PropertyRepoABC(ABCRepo,
                      RepoMixinsABC[PropertyDM,
                                    CreatePropertyDTO,
                                    RetrievePropertyDTO,
                                    UpdatePropertyDTO,
                                    DeletePropertyDTO]):
    ...
