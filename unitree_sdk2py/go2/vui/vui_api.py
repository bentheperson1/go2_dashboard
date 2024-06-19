from dataclasses import dataclass
"""
" service name
"""
VUI_SERVICE_NAME = "vui"


"""
" service api version
"""
VUI_API_VERSION = "1.0.0.1"


"""
" api id
"""
VUI_API_ID_SETSWITCH = 1001
VUI_API_ID_GETSWITCH = 1002
VUI_API_ID_SETVOLUME = 1003
VUI_API_ID_GETVOLUME = 1004
VUI_API_ID_SETBRIGHTNESS = 1005
VUI_API_ID_GETBRIGHTNESS = 1006
VUI_API_ID_LED_SET = 1007
VUI_API_ID_LED_QUIT = 1008

"""
" color
"""
@dataclass(frozen=True)
class VUI_COLOR:
    WHITE: str = 'white'
    RED: str = 'red'
    YELLOW: str = 'yellow'
    BLUE: str = 'blue'
    GREEN: str = 'green'
    CYAN: str = 'cyan'
    PURPLE: str = 'purple'
