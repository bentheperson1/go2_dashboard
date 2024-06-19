from enum import Enum
from .topics import DDS_TOPICS, WEBRTC_TOPICS

"""
" Enum ChannelType
"""
class ChannelType(Enum):
    SEND = 0
    RECV = 1

"""
" function GetClientChannelName
"""
def GetClientReqResChannelName(channel_name: str, serviceName: str, channelType: ChannelType):
    name = "rt/api/" + serviceName
    
    if channelType == ChannelType.SEND:
        name += "/request"
    else:
        name += "/response"

    if channel_name == 'DDS':
        return name
    elif channel_name == 'WEBRTC':
        if serviceName in WEBRTC_TOPICS:
            return name
        else: 
            raise ValueError(f"WEBRTC doesnt support this topic: {name}")

"""
" function GetClientChannelName
"""
def GetServerReqResChannelName(channel_name: str, serviceName: str, channelType: ChannelType):
    name = "rt/api/" + serviceName
    
    if channelType == ChannelType.SEND:
        name += "/response"
    else:
        name += "/request"

    if channel_name == 'DDS':
        return name
    elif channel_name == 'WEBRTC':
        if serviceName in WEBRTC_TOPICS:
            return name
        else: 
            raise ValueError(f"WEBRTC doesnt support this topic: {name}")