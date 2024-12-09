import logging
import json

from ...rpc.client import Client
from .gpt_api import *

from pydub import AudioSegment
import base64
import time
import uuid

"""
" class GPTClient
"""
class GPTClient(Client):
    default_service_name = GPT_SERVICE_NAME       

    def __init__(self, communicator, logger: logging.Logger = None, *args, **kwargs):
        self.logger = logger.getChild(self.__class__.__name__) if logger else logging.getLogger(self.__class__.__name__)
        self.communicator = communicator
        self.serviceName = GPTClient.default_service_name
        super().__init__(self.communicator, serviceName=self.serviceName, enabaleLease=False, logger=self.logger)

    def Init(self):
        # set api version
        self._SetApiVerson(GPT_API_VERSION)
        
        # regist api
        self._RegistApi(GPT_API_ID_COMMAND, 0)
    
    # 1002
    # Listen rt/gptflowfeedback for response
    def GPTSendCommand(self, command):
        parameter = command
        code, data = self._Call(GPT_API_ID_COMMAND, parameter)
        return code