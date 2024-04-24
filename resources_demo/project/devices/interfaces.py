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
                                PropertySelection,
                                UpdatePropertiesDTO,
                                PropertySelection]):
    ...


class ManufacturerControllerABC(ABCController,
                                ControllerMixinsABC[
                                    ManufacturerDM,
                                    CreateManufacturerDTO,
                                    ManufacturerSelection,
                                    UpdateManufacturerDTO,
                                    ManufacturerSelection]):
    ...

class DeviceTypeControllerABC(ABCController,
                              ControllerMixinsABC[
                                DeviceTypeDM,
                                CreateDeviceTypeDTO,
                                DeviceSelection,
                                UpdateDeviceTypeDTO,
                                DeviceSelection]):
    ...

class DeviceModelControllerABC(ABCController,
                               ControllerMixinsABC[
                                DeviceModelDM,
                                CreateDeviceModelDTO,
                                DeviceModelSelection,
                                UpdateDeviceModelDTO,
                                DeviceModelSelection]):
    ...


class DeviceControllerABC(ABCController,
                          ControllerMixinsABC[
                            DeviceDM,
                            CreateDeviceDTO,
                            DeviceSelection,
                            UpdateDeviceDTO,
                            DeviceSelection]):
    ...



# сервисы
class PropertyServiceABC(ABCService,
                             ServiceMixinsABC[
                               PropertyDM,
                               CreatePropertyDTO,
                               PropertySelection,
                               UpdatePropertiesDTO,
                               PropertySelection
                             ]):
    ...


class ManufacturerServiceABC(ABCService,
                             ServiceMixinsABC[
                               ManufacturerDM,
                               CreateManufacturerDTO,
                               ManufacturerSelection,
                               UpdateManufacturerDTO,
                               ManufacturerSelection
                             ]):
    ...

class DeviceTypeServiceABC(ABCService,
                             ServiceMixinsABC[
                               DeviceTypeDM,
                               CreateDeviceTypeDTO,
                               DeviceSelection,
                               UpdateDeviceTypeDTO,
                               DeviceSelection
                             ]):
    ...

class DeviceModelServiceABC(ABCService,
                             ServiceMixinsABC[
                               DeviceModelDM,
                               CreateDeviceModelDTO,
                               DeviceModelSelection,
                               UpdateDeviceModelDTO,
                               DeviceModelSelection
                             ]):
    ...


class DeviceServiceABC(ABCService,
                       ServiceMixinsABC[
                           DeviceDM,
                           CreateDeviceDTO,
                           DeviceSelection,
                           UpdateDeviceDTO,
                           DeviceSelection
                           ]):
    ...

# репозитории
class ManufacturerRepoABC(ABCRepo,
                          RepoMixinsABC[
                            ManufacturerDM,
                            CreateManufacturerDTO,
                            ManufacturerSelection,
                            UpdateManufacturerDTO,
                            ManufacturerSelection
                          ]):
    ...


class DeviceTypeRepoABC(ABCRepo,
                          RepoMixinsABC[
                            DeviceTypeDM,
                            CreateDeviceTypeDTO,
                            DeviceSelection,
                            UpdateDeviceTypeDTO,
                            DeviceSelection
                          ]):
    ...


class DeviceModelRepoABC(ABCRepo,
                          RepoMixinsABC[
                            DeviceModelDM,
                            CreateDeviceModelDTO,
                            DeviceModelSelection,
                            UpdateDeviceModelDTO,
                            DeviceModelSelection
                          ]):
    ...


class DeviceRepoABC(ABCRepo,
                      RepoMixinsABC[DeviceDM,
                                    CreateDeviceDTO,
                                    DeviceSelection,
                                    UpdateDeviceDTO,
                                    DeviceSelection]):
    ...


class PropertyRepoABC(ABCRepo,
                      RepoMixinsABC[PropertyDM,
                                    CreatePropertyDTO,
                                    PropertySelection,
                                    UpdatePropertiesDTO,
                                    PropertySelection]):
    ...
