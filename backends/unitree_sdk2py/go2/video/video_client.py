import json

from ...rpc.client import Client
from .video_api import *

import logging

"""
" class VideoClient
"""
class VideoClient(Client):
    default_service_name = VIDEO_SERVICE_NAME
    
    def __init__(self, communicator, logger: logging.Logger = None, *args, **kwargs):
        self.logger = logger.getChild(self.__class__.__name__) if logger else logging.getLogger(self.__class__.__name__)
        self.service_name = VideoClient.default_service_name
        super().__init__(communicator=communicator, serviceName=self.service_name, enabaleLease=False, logger=self.logger)
    
    def Init(self):
        # set api version
        self._SetApiVerson(VIDEO_API_VERSION)
        # regist api
        self._RegistApi(VIDEO_API_ID_GETIMAGESAMPLE, 0)

    # 1001
    def GetImageSample(self):
        return self._CallBinary(VIDEO_API_ID_GETIMAGESAMPLE, [])
