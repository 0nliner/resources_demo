from typing import Optional
from pydantic import BaseModel
from lib.interfaces import DTOBase, BaseSelection

from core import EditableMetadata, IdSelection, DateSelection, DefaultMetadataSelection


class PropertiesBaseSelection(IdSelection, DateSelection, DefaultMetadataSelection):
    ...

# селекшены
class PropertySelection(PropertiesBaseSelection):
    ...

class DeviceModelSelection(PropertiesBaseSelection):
    ...

class ManufacturerSelection(PropertiesBaseSelection):
    ...

class DeviceSelection(PropertiesBaseSelection):
    ...


############### DTO на обновление
class UpdatePropertyPayload(EditableMetadata, BaseModel):
    node_id: Optional[int]
    device_id: Optional[int]


class UpdatePropertiesDTO(DTOBase):
    id: int
    payload: UpdatePropertyPayload


class UpdateDevicePayload(EditableMetadata, BaseModel):
    ...


class UpdateDeviceDTO(DTOBase):
    id: int
    payload: UpdateDevicePayload


class UpdateManufacturerPayload(BaseModel):
    ...


class UpdateManufacturerDTO(DTOBase):
    id: int
    payload: UpdateManufacturerPayload


class UpdateDeviceTypePayload(BaseModel):
    ...


class UpdateDeviceTypeDTO(DTOBase):
    id: int
    payload: UpdateDeviceTypePayload


class UpdateDeviceModelPayload(BaseModel):
    ...


class UpdateDeviceModelDTO(DTOBase):
    id: int
    payload: UpdateDeviceModelPayload


# dto на создание объектов
class CreatePropertyDTO(EditableMetadata, BaseModel):
    node_id: int

class CreateDeviceDTO(EditableMetadata, BaseModel):
    property_id: int


class CreateManufacturerDTO(DTOBase):
    ...


class CreateDeviceTypeDTO(DTOBase):
    ...



class CreateDeviceModelDTO(DTOBase):
    ...
