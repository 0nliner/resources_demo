from typing import Optional
from pydantic import BaseModel
from lib import DTOBase

from core import EditableMetadata


class CreatePropertyDTO(EditableMetadata, BaseModel):
    node_id: int


class UpdatePropertyPayload(EditableMetadata, BaseModel):
    node_id: Optional[int]
    device_id: Optional[int]


class UpdatePropertyDTO(DTOBase):
    id: int
    payload: UpdatePropertyPayload


class RetrievePropertyDTO(DTOBase):
    id: int


class DeletePropertyDTO(DTOBase):
    id: int


class CreateDeviceDTO(EditableMetadata, BaseModel):
    property_id: int


class RetrieveDeviceDTO(DTOBase):
    id: int


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



class DeleteDeviceDTO(DTOBase):
    id: int



class CreateManufacturerDTO(DTOBase):
    ...


class RetrieveManufacturerDTO(DTOBase):
    ...


class DeleteManufacturerDTO(DTOBase):
    ...


class CreateDeviceTypeDTO(DTOBase):
    ...


class RetrieveDeviceTypeDTO(DTOBase):
    id: int


class DeleteDeviceTypeDTO(DTOBase):
    id: int


class CreateDeviceModelDTO(DTOBase):
    ...


class RetrieveDeviceModelDTO(DTOBase):
    id: int


class DeleteDeviceModelDTO(DTOBase):
    id: int


class CreateManufacturerDTO(DTOBase):
    ...


class RetrieveManufacturerDTO(DTOBase):
    id: int


class DeleteManufacturerDTO(DTOBase):
    id: int


class CreateDeviceTypeDTO(DTOBase):
    ...


class RetrieveDeviceTypeDTO(DTOBase):
    id: int


class DeleteDeviceTypeDTO(DTOBase):
    id: int


class CreateDeviceModelDTO(DTOBase):
    ...


class RetrieveDeviceModelDTO(DTOBase):
    id: int


class DeleteDeviceModelDTO(DTOBase):
    id: int

