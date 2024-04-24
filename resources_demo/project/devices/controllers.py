from archtool.layers.default_layer_interfaces import ABCController
from lib.interfaces import ControllerMixins
from .interfaces import *
from .dtos import *
from .datamappers import *


class PropertyController(PropertyControllerABC,
                            ControllerMixins[
                                PropertyDM,
                                CreatePropertyDTO,
                                PropertySelection,
                                UpdatePropertiesDTO,
                                PropertySelection]):

    default_service: PropertyServiceABC


class ManufacturerController(ManufacturerControllerABC,
                                ControllerMixins[
                                    ManufacturerDM,
                                    CreateManufacturerDTO,
                                    ManufacturerSelection,
                                    UpdateManufacturerDTO,
                                    ManufacturerSelection]):

    default_service: ManufacturerServiceABC


class DeviceTypeController(DeviceTypeControllerABC,
                              ControllerMixins[
                                DeviceTypeDM,
                                CreateDeviceTypeDTO,
                                DeviceSelection,
                                UpdateDeviceTypeDTO,
                                DeviceSelection]):

    default_service: DeviceTypeServiceABC


class DeviceModelController(DeviceModelControllerABC,
                               ControllerMixins[
                                DeviceModelDM,
                                CreateDeviceModelDTO,
                                DeviceModelSelection,
                                UpdateDeviceModelDTO,
                                DeviceModelSelection]):

    default_service: DeviceModelServiceABC


class DeviceController(DeviceControllerABC,
                          ControllerMixins[
                            DeviceDM,
                            CreateDeviceDTO,
                            DeviceSelection,
                            UpdateDeviceDTO,
                            DeviceSelection]):

    default_service: DeviceServiceABC
