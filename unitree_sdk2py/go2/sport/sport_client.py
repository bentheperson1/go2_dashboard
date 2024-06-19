import json

from ...rpc.client import Client
from .sport_api import *

import logging

"""
" SPORT_PATH_POINT_SIZE
"""
SPORT_PATH_POINT_SIZE = 30


"""
" class PathPoint
"""
class PathPoint:
    def __init__(self, timeFromStart: float, x: float, y: float, yaw: float, vx: float, vy: float, vyaw: float):
        self.timeFromStart = timeFromStart
        self.x = x
        self.y = y
        self.yaw = yaw
        self.vx = vx
        self.vy = vy
        self.vyaw = vyaw


"""
" class SportClient
"""
class SportClient(Client):
    default_service_name = SPORT_SERVICE_NAME          

    def __init__(self, communicator, logger: logging.Logger = None, *args, **kwargs):
        self.enableLease = kwargs.pop('enableLease', False) 
        self.logger = logger.getChild(self.__class__.__name__) if logger else logging.getLogger(self.__class__.__name__)
        self.serviceName = SportClient.default_service_name
        super().__init__(communicator, self.serviceName, self.enableLease, self.logger)

    def Init(self):
        # set api version
        self._SetApiVerson(SPORT_API_VERSION)
        
        # regist api
        self._RegistApi(SPORT_API_ID_DAMP, 0)
        self._RegistApi(SPORT_API_ID_BALANCESTAND, 0)
        self._RegistApi(SPORT_API_ID_STOPMOVE, 0)
        self._RegistApi(SPORT_API_ID_STANDUP, 0)
        self._RegistApi(SPORT_API_ID_STANDDOWN, 0)
        self._RegistApi(SPORT_API_ID_RECOVERYSTAND, 0)
        self._RegistApi(SPORT_API_ID_EULER, 0)
        self._RegistApi(SPORT_API_ID_MOVE, 0)
        self._RegistApi(SPORT_API_ID_SIT, 0)
        self._RegistApi(SPORT_API_ID_RISESIT, 0)
        self._RegistApi(SPORT_API_ID_SWITCHGAIT, 0)
        self._RegistApi(SPORT_API_ID_TRIGGER, 0)
        self._RegistApi(SPORT_API_ID_BODYHEIGHT, 0)
        self._RegistApi(SPORT_API_ID_FOOTRAISEHEIGHT, 0)
        self._RegistApi(SPORT_API_ID_SPEEDLEVEL, 0)
        self._RegistApi(SPORT_API_ID_HELLO, 0)
        self._RegistApi(SPORT_API_ID_STRETCH, 0)
        self._RegistApi(SPORT_API_ID_TRAJECTORYFOLLOW, 0)
        self._RegistApi(SPORT_API_ID_CONTINUOUSGAIT, 0)
        # self._RegistApi(SPORT_API_ID_CONTENT, 0)
        self._RegistApi(SPORT_API_ID_WALLOW, 0)
        self._RegistApi(SPORT_API_ID_DANCE1, 0)
        self._RegistApi(SPORT_API_ID_DANCE2, 0)
        # self._RegistApi(SPORT_API_ID_GETBODYHEIGHT, 0)
        # self._RegistApi(SPORT_API_ID_GETFOOTRAISEHEIGHT, 0)
        # self._RegistApi(SPORT_API_ID_GETSPEEDLEVEL, 0)
        self._RegistApi(SPORT_API_ID_SWITCHJOYSTICK, 0)
        self._RegistApi(SPORT_API_ID_POSE, 0)
        self._RegistApi(SPORT_API_ID_SCRAPE, 0)
        self._RegistApi(SPORT_API_ID_FRONTFLIP, 0)
        self._RegistApi(SPORT_API_ID_FRONTJUMP, 0)
        self._RegistApi(SPORT_API_ID_FRONTPOUNCE, 0)
        self._RegistApi(SPORT_API_ID_WIGGLEHIPS, 0)
        self._RegistApi(SPORT_API_ID_GETSTATE, 0)
        self._RegistApi(SPORT_API_ID_ECONOMICGAIT, 0)
        self._RegistApi(SPORT_API_ID_HEART, 0)
        self._RegistApi(SPORT_API_ID_LEADFOLLOW, 0)

        self._RegistApi(SPORT_API_ID_HANDSTAND, 0)
        self._RegistApi(SPORT_API_ID_CROSSSTEP, 0)
        self._RegistApi(SPORT_API_ID_ONESIDEDSTEP, 0)
        self._RegistApi(SPORT_API_ID_BOUND, 0)

        self._RegistApi(SPORT_API_ID_STANDOUT, 0)
        self._RegistApi(SPORT_API_ID_SET_AUTO_ROLL_RECOVERY, 0)
        self._RegistApi(SPORT_API_ID_GET_AUTO_ROLL_RECOVERY, 0)

    # 1001
    def Damp(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_DAMP, parameter)
        return code
    
    # 1002
    def BalanceStand(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_BALANCESTAND, parameter)
        return code
    
    # 1003
    def StopMove(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_STOPMOVE, parameter)
        return code

    # 1004
    def StandUp(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_STANDUP, parameter)
        return code

    # 1005
    def StandDown(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_STANDDOWN, parameter)
        return code

    # 1006
    def RecoveryStand(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_RECOVERYSTAND, parameter)
        return code

    # 1007
    def Euler(self, roll: float, pitch: float, yaw: float):
        p = {}
        p["x"] = roll
        p["y"] = pitch
        p["z"] = yaw
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_EULER, parameter)
        return code

    # 1008
    def Move(self, vx: float, vy: float, vyaw: float):
        p = {}
        p["x"] = vx
        p["y"] = vy
        p["z"] = vyaw
        parameter = json.dumps(p)
        code = self._CallNoReply(SPORT_API_ID_MOVE, parameter)
        return code

    # 1009
    def Sit(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_SIT, parameter)
        return code

    #1010
    def RiseSit(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_RISESIT, parameter)
        return code

    # 1011
    def SwitchGait(self, t: int):
        p = {}
        p["data"] = t
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_SWITCHGAIT, parameter)
        return code

    # 1012
    def Trigger(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_TRIGGER, parameter)
        return code

    # 1013
    def BodyHeight(self, height: float):
        p = {}
        p["data"] = height
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_BODYHEIGHT, parameter)
        return code

    # 1014
    def FootRaiseHeight(self, height: float):
        p = {}
        p["data"] = height
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_FOOTRAISEHEIGHT, parameter)
        return code

    # 1015
    def SpeedLevel(self, level: int):
        p = {}
        p["data"] = level
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_SPEEDLEVEL, parameter)
        return code

    # 1016
    def Hello(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_HELLO, parameter)
        return code

    # 1017
    def Stretch(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_STRETCH, parameter)
        return code

    # 1018
    def TrajectoryFollow(self, path: list):
        l = len(path)
        if l != SPORT_PATH_POINT_SIZE:
            return SPORT_ERR_CLIENT_POINT_PATH

        path_p = []
        for i in range(l):
            point = path[i]
            p = {}
            p["t_from_start"] = point.timeFromStart
            p["x"] = point.x
            p["y"] = point.y
            p["yaw"] = point.yaw
            p["vx"] = point.vx
            p["vy"] = point.vy
            p["vyaw"] = point.vyaw
            path_p.append(p)
            
        parameter = json.dumps(path_p)
        code = self._CallNoReply(SPORT_API_ID_TRAJECTORYFOLLOW, parameter)
        return code

    # 1019
    def ContinuousGait(self, flag: int):
        p = {}
        p["data"] = flag
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_CONTINUOUSGAIT, parameter)
        return code

    # # 1020
    # def Content(self):
    #     p = {}
    #     parameter = json.dumps(p)
    #     code, data = self._Call(SPORT_API_ID_CONTENT, parameter)
    #     return code
    
    # 1021
    def Wallow(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_WALLOW, parameter)
        return code

    # 1022
    def Dance1(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_DANCE1, parameter)
        return code

    # 1023
    def Dance2(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_DANCE2, parameter)
        return code

    # 1025
    def GetFootRaiseHeight(self):
        p = {}
        parameter = json.dumps(p)
        
        code, data = self._Call(SPORT_API_ID_GETFOOTRAISEHEIGHT, parameter)
        
        if code == 0:
            d = json.loads(data)
            return code, d["data"]
        else:
            return code, None
            

    # 1026
    def GetSpeedLevel(self):
        p = {}
        parameter = json.dumps(p)
        
        code, data = self._Call(SPORT_API_ID_GETSPEEDLEVEL, parameter)
        
        if code == 0:
            d = json.loads(data)
            return code, d["data"]
        else:
            return code, None

    # 1027
    def SwitchJoystick(self, on: bool):
        p = {}
        p["data"] = on
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_SWITCHJOYSTICK, parameter)
        return code

    # 1028
    def Pose(self, flag: bool):
        p = {}
        p["data"] = flag
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_POSE, parameter)
        return code

    # 1029
    def Scrape(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_SCRAPE, parameter)
        return code

    # 1030
    def FrontFlip(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_FRONTFLIP, parameter)
        return code

    # 1031
    def FrontJump(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_FRONTJUMP, parameter)
        return code

    # 1032
    def FrontPounce(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_FRONTPOUNCE, parameter)
        return code

    # 1033
    def WiggleHips(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_WIGGLEHIPS, parameter)
        return code

    # 1034
    def GetState(self, keys: list):
        parameter = json.dumps(keys)
        code, data = self._Call(SPORT_API_ID_GETSTATE, parameter)
        if code == 0:
            return code, json.loads(data)
        else:
            return code, None

    # 1035
    def EconomicGait(self, flag: bool):
        p = {}
        p["data"] = flag
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_ECONOMICGAIT, parameter)
        return code

    # 1036
    def Heart(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_HEART, parameter)
        return code

    # 1045
    def LeadFollow(self, on: bool):
        p = {}
        p["data"] = on
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_LEADFOLLOW, parameter)
        return code
    
    #below API only works while in advanced mode

    #1301
    def HandStand(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_HANDSTAND, parameter)
        return code
    
    #1302
    def CrossStep(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_CROSSSTEP, parameter)
        return code
    
    #1303
    def OneSideStep(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_ONESIDEDSTEP, parameter)
        return code
    
    #1304
    def Bound(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_BOUND, parameter)
        return code
    
    #below API only works while in ai mode
    #1038
    def AutoSwitchMoveMode(self, on: bool):
        p = {}
        p["data"] = on
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_AUTO_SWITCH_MOVE_MODE, parameter)
        return code
    
    #1039
    def StandOut(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_STANDOUT, parameter)
        return code
    
    #1040
    def SetAutoRollrecovery(self, on: bool):
        p = {}
        p["data"] = on
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_SET_AUTO_ROLL_RECOVERY, parameter)
        return code
    
    #1041
    def GetAutoRollrecovery(self):
        p = {}
        parameter = json.dumps(p)
        code, data = self._Call(SPORT_API_ID_GET_AUTO_ROLL_RECOVERY, parameter)
        if code == 0:
            return code, json.loads(data)
        else:
            return code, None