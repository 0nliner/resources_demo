from archtool.layers.default_layer_interfaces import ABCController
from lib.interfaces import ControllerMixins
from .interfaces import *
from .dtos import *
from .datamappers import *


class PropertyController(PropertyControllerABC,
                            ControllerMixins[
                                PropertyDM,
                                CreatePropertyDTO,
                                RetrievePropertyDTO,
                                UpdatePropertyDTO,
                                DeletePropertyDTO]):

    default_service: PropertyServiceABC


class ManufacturerController(ManufacturerControllerABC,
                                ControllerMixins[
                                    ManufacturerDM,
                                    CreateManufacturerDTO,
                                    RetrieveManufacturerDTO,
                                    UpdateManufacturerDTO,
                                    DeleteManufacturerDTO]):

    default_service: ManufacturerServiceABC


class DeviceTypeController(DeviceTypeControllerABC,
                              ControllerMixins[
                                DeviceTypeDM,
                                CreateDeviceTypeDTO,
                                RetrieveDeviceTypeDTO,
                                UpdateDeviceTypeDTO,
                                DeleteDeviceTypeDTO]):

    default_service: DeviceTypeServiceABC


class DeviceModelController(DeviceModelControllerABC,
                               ControllerMixins[
                                DeviceModelDM,
                                CreateDeviceModelDTO,
                                RetrieveDeviceModelDTO,
                                UpdateDeviceModelDTO,
                                DeleteDeviceModelDTO]):

    default_service: DeviceModelServiceABC


class DeviceController(DeviceControllerABC,
                          ControllerMixins[
                            DeviceDM,
                            CreateDeviceDTO,
                            RetrieveDeviceDTO,
                            UpdateDeviceDTO,
                            DeleteDeviceDTO]):

    default_service: DeviceServiceABC
