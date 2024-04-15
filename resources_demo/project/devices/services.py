from lib.interfaces import ServiceMixins

from .interfaces import *
from .dtos import *
from .datamappers import *

from exceptions import NotExist


class PropertyService(PropertyServiceABC,
                      ServiceMixins[
                          PropertyDM,
                          CreatePropertyDTO,
                          RetrievePropertyDTO,
                          UpdatePropertyDTO,
                          DeletePropertyDTO]):

    default_repo: PropertyRepoABC
    property_repo: PropertyRepoABC
    device_repo: DeviceRepoABC

    async def update(self, data: UpdatePropertyDTO) -> PropertyDM:
        # проверяем существует ли устройство, которое хотим подвязать к объекту,
        # если объект не существует - райзим ошибку
        await self.property_repo.get(data.id, raise_on_none=True)
        if data.payload.device_id:
            await self.device_repo.get(data.payload.device_id, raise_on_none=True)
        # проверяем существует ли нода, которую хотим подвязать к объекту
        if data.payload.node_id:
            await self.device_repo.get(data.payload.node_id, raise_on_none=True)
        updated_object = await self.property_repo.update(data)
        return updated_object


class DeviceService(DeviceServiceABC,
                    ServiceMixins[
                          DeviceDM,
                          CreateDeviceDTO,
                          RetrieveDeviceDTO,
                          UpdateDeviceDTO,
                          DeleteDeviceDTO]):

    default_repo: DeviceRepoABC


class ManufacturerService(ManufacturerServiceABC,
                          ServiceMixins[
                            ManufacturerDM,
                            CreateManufacturerDTO,
                            RetrieveManufacturerDTO,
                            UpdateManufacturerDTO,
                            DeleteManufacturerDTO]):

    default_repo: ManufacturerRepoABC


class DeviceTypeService(DeviceTypeServiceABC,
                          ServiceMixins[
                            DeviceTypeDM,
                            CreateDeviceTypeDTO,
                            RetrieveDeviceTypeDTO,
                            UpdateDeviceTypeDTO,
                            DeleteDeviceTypeDTO]):

    default_repo: DeviceTypeRepoABC


class DeviceModelService(DeviceModelServiceABC,
                          ServiceMixins[
                            DeviceModelDM,
                            CreateDeviceModelDTO,
                            RetrieveDeviceModelDTO,
                            UpdateDeviceModelDTO,
                            DeleteDeviceModelDTO]):

    default_repo: DeviceModelRepoABC


class DeviceService(DeviceServiceABC,
                          ServiceMixins[
                            DeviceDM,
                            CreateDeviceDTO,
                            RetrieveDeviceDTO,
                            UpdateDeviceDTO,
                            DeleteDeviceDTO]):

    default_repo: DeviceRepoABC

