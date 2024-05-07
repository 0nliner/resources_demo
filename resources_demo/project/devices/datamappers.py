from typing import Optional
from core import EditableMetadata
from lib.interfaces import DMBase


class PropertyDM(EditableMetadata, DMBase):
    device_id: Optional[int]
    node_id: Optional[int]


class DeviceDM(DMBase):
    device_model_id: Optional[int]
    property_id: Optional[int]
    icon_tag: Optional[str]


class ManufacturerDM(DMBase):
    example: str


class DeviceTypeDM(DMBase):
    example: str


class DeviceModelDM(DMBase):
    example: str

