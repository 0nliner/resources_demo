from sqlalchemy.orm import sessionmaker

from lib.interfaces import RepoMixins

from .interfaces import *
from .models import *
from .dtos import *
from .datamappers import *


class PropertyRepo(PropertyRepoABC,
                   RepoMixins[PropertyDM,
                              CreatePropertyDTO,
                              PropertySelection,
                              UpdatePropertiesDTO,
                              PropertySelection]):
    model = Property
    session_maker: sessionmaker



class ManufacturerRepo(ManufacturerRepoABC,
                          RepoMixins[
                            ManufacturerDM,
                            CreateManufacturerDTO,
                            ManufacturerSelection,
                            UpdateManufacturerDTO,
                            ManufacturerSelection
                          ]):

    model = Manufacturer
    session_maker: sessionmaker
    

class DeviceTypeRepo(DeviceTypeRepoABC,
                          RepoMixins[
                            DeviceTypeDM,
                            CreateDeviceTypeDTO,
                            DeviceSelection,
                            UpdateDeviceTypeDTO,
                            DeviceSelection
                          ]):

    model = DeviceType
    session_maker: sessionmaker
    

class DeviceModelRepo(DeviceModelRepoABC,
                          RepoMixins[
                            DeviceModelDM,
                            CreateDeviceModelDTO,
                            DeviceModelSelection,
                            UpdateDeviceModelDTO,
                            DeviceModelSelection
                          ]):

    model = DeviceModel
    session_maker: sessionmaker
    


class DeviceRepo(DeviceRepoABC,
                      RepoMixins[DeviceDM,
                                    CreateDeviceDTO,
                                    DeviceSelection,
                                    UpdateDeviceDTO,
                                    DeviceSelection]):

    model = Device
    session_maker: sessionmaker
    
