import json

from ...rpc.client import Client
from .vui_api import *
import logging


"""
" class VideoClient
"""
class VuiClient(Client):
    default_service_name = VUI_SERVICE_NAME

    def __init__(self, communicator, logger: logging.Logger = None, *args, **kwargs):
        self.service_name = VuiClient.default_service_name
        self.logger = logger.getChild(self.__class__.__name__) if logger else logging.getLogger(self.__class__.__name__)
        super().__init__(communicator=communicator, serviceName=self.service_name, enabaleLease=False, logger=self.logger)

    def Init(self):
        # set api version
        self._SetApiVerson(VUI_API_VERSION)
        # regist api
        self._RegistApi(VUI_API_ID_SETSWITCH, 0)
        self._RegistApi(VUI_API_ID_GETSWITCH, 0)
        self._RegistApi(VUI_API_ID_SETVOLUME, 0)
        self._RegistApi(VUI_API_ID_GETVOLUME, 0)
        self._RegistApi(VUI_API_ID_SETBRIGHTNESS, 0)
        self._RegistApi(VUI_API_ID_GETBRIGHTNESS, 0)
        self._RegistApi(VUI_API_ID_LED_SET, 0)
        self._RegistApi(VUI_API_ID_LED_QUIT, 0)

    # 1001
    def SetSwitch(self, enable: int):
        p = {}
        p["enable"] = enable
        parameter = json.dumps(p)

        code, data = self._Call(VUI_API_ID_SETSWITCH, parameter)
        return code

    # 1002
    def GetSwitch(self):
        p = {}
        parameter = json.dumps(p)

        code, data = self._Call(VUI_API_ID_GETSWITCH, parameter)
        if code == 0:
            d = json.loads(data)
            return code, d["enable"]
        else:
            return code, None

    # 1003
    def SetVolume(self, level: int):
        p = {}
        p["volume"] = level
        parameter = json.dumps(p)

        code, data = self._Call(VUI_API_ID_SETVOLUME, parameter)
        return code

    # 1006
    def GetVolume(self):
        p = {}
        parameter = json.dumps(p)

        code, data = self._Call(VUI_API_ID_GETVOLUME, parameter)
        if code == 0:
            d = json.loads(data)
            return code, d["volume"]
        else:
            return code, None

    # 1005
    def SetBrightness(self, level: int):
        p = {}
        p["brightness"] = level
        parameter = json.dumps(p)

        code, data = self._Call(VUI_API_ID_SETBRIGHTNESS, parameter)
        return code

    # 1006
    def GetBrightness(self):
        p = {}
        parameter = json.dumps(p)

        code, data = self._Call(VUI_API_ID_GETBRIGHTNESS, parameter)
        if code == 0:
            d = json.loads(data)
            return code, d["brightness"]
        else:
            return code, None
    
    # 1007
    def SetLed(self, color: VUI_COLOR, time=5, flash_cycle=None):
        p = {}
        p["color"] = color
        p["time"] = time
        if flash_cycle:
            p["flash_cycle"] = flash_cycle
        parameter = json.dumps(p)
        code, data = self._Call(VUI_API_ID_LED_SET, parameter)
        return code
    
    # 1008
    def QuitLed(self, level: int):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(VUI_API_ID_LED_QUIT, parameter)
        return code