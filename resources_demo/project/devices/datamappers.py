from typing import Optional
from pydantic import BaseModel, Field
from core import EditableMetadata


class PropertyDM(EditableMetadata, BaseModel):
    device_id: Optional[int]
    node_id: Optional[int]


class DeviceDM(BaseModel):
    device_model_id: Optional[int]
    property_id: Optional[int]
    icon_tag: Optional[str]


class ManufacturerDM(BaseModel):
    ...


class DeviceTypeDM(BaseModel):
    ...


class DeviceModelDM(BaseModel):
    ...


class ManufacturerDM(BaseModel):
    ...


class DeviceTypeDM(BaseModel):
    ...


class DeviceModelDM(BaseModel):
    ...

