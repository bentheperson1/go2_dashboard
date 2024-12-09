import logging
import json

from ...rpc.client import Client
from .motion_switcher_api import *

"""
" class MotionSwitcherClient
"""
class MotionSwitcherClient(Client):
    default_service_name = MOTION_SWITCHER_SERVICE_NAME       

    def __init__(self, communicator, logger: logging.Logger = None, *args, **kwargs):
        self.logger = logger.getChild(self.__class__.__name__) if logger else logging.getLogger(self.__class__.__name__)
        self.serviceName = MotionSwitcherClient.default_service_name
        super().__init__(communicator, serviceName=self.serviceName, enabaleLease=False, logger=self.logger)

    def Init(self):
        # set api version
        self._SetApiVerson(MOTION_SWITCHER_API_VERSION)
        
        # regist api
        self._RegistApi(MOTION_SWITCHER_API_ID_GET_MODE, 0)
        self._RegistApi(MOTION_SWITCHER_API_ID_SET_MODE, 0)
        self._RegistApi(MOTION_SWITCHER_API_ID_RELEASE_MODE, 0)
        self._RegistApi(MOTION_SWITCHER_API_ID_GET_SILENT, 0)
        self._RegistApi(MOTION_SWITCHER_API_ID_SET_SILENT, 0)

    # 1001
    # Get current sport mode: normal or advanced or ai
    def GetMode(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(MOTION_SWITCHER_API_ID_GET_MODE, parameter)
        return code

    # 1002
    # Set current sport mode: normal or advanced or ai
    def SetMode(self, mode: str):
        p = {}
        p["name"] = mode
        parameter = json.dumps(p)
        code, data = self._Call(MOTION_SWITCHER_API_ID_SET_MODE, parameter)
        return code
    
    # 1003
    # Disables both services: advanced and normal and ai
    # If flag set to True then dumps imediatly, otherwise does a soft StandDown movement
    def ReleaseMode(self, flag: bool):
        p = {}
        p["sample"] = flag
        parameter = json.dumps(p)
        code, data = self._Call(MOTION_SWITCHER_API_ID_RELEASE_MODE, parameter)
        return code
    
    # 1004
    # If true after the boot up none of the sport services would be launched. Perfect for developing
    def SetSilent(self, flag: bool):
        p = {}
        p["silent"] = flag
        parameter = json.dumps(p)
        code, data = self._Call(MOTION_SWITCHER_API_ID_SET_SILENT, parameter)
        return code
    
    # 1005
    def GetSilent(self, flag: bool):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(MOTION_SWITCHER_API_ID_GET_SILENT, parameter)
        return code