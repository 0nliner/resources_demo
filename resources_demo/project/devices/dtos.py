from typing import Optional
from pydantic import BaseModel
from core import EditableMetadata


class CreatePropertyDTO(EditableMetadata, BaseModel):
    node_id: int


class UpdatePropertyPayload(EditableMetadata, BaseModel):
    node_id: Optional[int]
    device_id: Optional[int]


class UpdatePropertyDTO(BaseModel):
    id: int
    payload: UpdatePropertyPayload


class RetrievePropertyDTO(BaseModel):
    id: int


class DeletePropertyDTO(BaseModel):
    id: int


class CreateDeviceDTO(EditableMetadata, BaseModel):
    property_id: int


class RetrieveDeviceDTO(BaseModel):
    id: int


class UpdateDevicePayload(EditableMetadata, BaseModel):
    ...


class UpdateDeviceDTO(BaseModel):
    id: int
    payload: UpdateDevicePayload


class UpdateManufacturerPayload(BaseModel):
    ...


class UpdateManufacturerDTO(BaseModel):
    id: int
    payload: UpdateManufacturerPayload


class UpdateDeviceTypePayload(BaseModel):
    ...


class UpdateDeviceTypeDTO(BaseModel):
    id: int
    payload: UpdateDeviceTypePayload


class UpdateDeviceModelPayload(BaseModel):
    ...


class UpdateDeviceModelDTO(BaseModel):
    id: int
    payload: UpdateDeviceModelPayload



class DeleteDeviceDTO(BaseModel):
    id: int



class CreateManufacturerDTO(BaseModel):
    ...


class RetrieveManufacturerDTO(BaseModel):
    ...


class DeleteManufacturerDTO(BaseModel):
    ...


class CreateDeviceTypeDTO(BaseModel):
    ...


class RetrieveDeviceTypeDTO(BaseModel):
    id: int


class DeleteDeviceTypeDTO(BaseModel):
    id: int


class CreateDeviceModelDTO(BaseModel):
    ...


class RetrieveDeviceModelDTO(BaseModel):
    id: int


class DeleteDeviceModelDTO(BaseModel):
    id: int


class CreateManufacturerDTO(BaseModel):
    ...


class RetrieveManufacturerDTO(BaseModel):
    id: int


class DeleteManufacturerDTO(BaseModel):
    id: int


class CreateDeviceTypeDTO(BaseModel):
    ...


class RetrieveDeviceTypeDTO(BaseModel):
    id: int


class DeleteDeviceTypeDTO(BaseModel):
    id: int


class CreateDeviceModelDTO(BaseModel):
    ...


class RetrieveDeviceModelDTO(BaseModel):
    id: int


class DeleteDeviceModelDTO(BaseModel):
    id: int

