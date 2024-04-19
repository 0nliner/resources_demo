from sqlalchemy.orm import sessionmaker

from lib.interfaces import RepoMixins

from .interfaces import *
from .models import *
from .dtos import *
from .datamappers import *


class PropertyRepo(PropertyRepoABC,
                   RepoMixins[PropertyDM,
                              CreatePropertyDTO,
                              RetrievePropertyDTO,
                              UpdatePropertyDTO,
                              DeletePropertyDTO]):
    model = Property
    session_maker: sessionmaker



class ManufacturerRepo(ManufacturerRepoABC,
                          RepoMixins[
                            ManufacturerDM,
                            CreateManufacturerDTO,
                            RetrieveManufacturerDTO,
                            UpdateManufacturerDTO,
                            DeleteManufacturerDTO
                          ]):

    model = Manufacturer
    session_maker: sessionmaker
    

class DeviceTypeRepo(DeviceTypeRepoABC,
                          RepoMixins[
                            DeviceTypeDM,
                            CreateDeviceTypeDTO,
                            RetrieveDeviceTypeDTO,
                            UpdateDeviceTypeDTO,
                            DeleteDeviceTypeDTO
                          ]):

    model = DeviceType
    session_maker: sessionmaker
    

class DeviceModelRepo(DeviceModelRepoABC,
                          RepoMixins[
                            DeviceModelDM,
                            CreateDeviceModelDTO,
                            RetrieveDeviceModelDTO,
                            UpdateDeviceModelDTO,
                            DeleteDeviceModelDTO
                          ]):

    model = DeviceModel
    session_maker: sessionmaker
    


class DeviceRepo(DeviceRepoABC,
                      RepoMixins[DeviceDM,
                                    CreateDeviceDTO,
                                    RetrieveDeviceDTO,
                                    UpdateDeviceDTO,
                                    DeleteDeviceDTO]):

    model = Device
    session_maker: sessionmaker
    
