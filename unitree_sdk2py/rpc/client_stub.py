import time

from enum import Enum
from threading import Thread, Condition

from ..core.channel_name import ChannelType, GetClientReqResChannelName
from .request_future import RequestFuture, RequestFutureQueue

import logging

"""
" class ClientStub
"""
class ClientStub:
    def __init__(self, communicator, serviceName: str, logger: logging.Logger = None):
        self.logger = logger.getChild(self.__class__.__name__) if logger else logging.getLogger(self.__class__.__name__)
        self.__serviceName = serviceName
        self.__futureQueue = None

        self.__sendChannel = None
        self.__recvChannel = None
        self.__communicator = communicator

    def Init(self):
        factory = self.__communicator.ChannelFactory()
        self.__futureQueue = RequestFutureQueue()

        self.Request = factory.dataclass.get_data_class('Request_')
        self.Response = factory.dataclass.get_data_class('Response_')

        # create channel
        self.__sendChannel = factory.CreateSendChannel(GetClientReqResChannelName(factory.channel_name, self.__serviceName, ChannelType.SEND), self.Request)
        self.__recvChannel = factory.CreateRecvChannel(GetClientReqResChannelName(factory.channel_name, self.__serviceName, ChannelType.RECV), self.Response,
                                    self.__ResponseHandler,10)
        time.sleep(0.5)


    def Send(self, request, timeout: float):
        if self.__sendChannel.Write(request, timeout):
            return True
        else:
            self.logger.error("[ClientStub] send error. id: %s", request.header.identity.id)
            return False

    def SendRequest(self, request, timeout: float):
        id = request.header.identity.id

        future = RequestFuture()
        future.SetRequestId(id)
        self.__futureQueue.Set(id, future)

        if self.__sendChannel.Write(request, timeout):
            return future
        else:
            self.logger.error("[ClientStub] send request error. id: %s", request.header.identity.id)
            self.__futureQueue.Remove(id)
            return None

    def RemoveFuture(self, requestId: int):
        self.__futureQueue.Remove(requestId)

    def __ResponseHandler(self, response):
        id = response.header.identity.id
        # apiId = response.header.identity.api_id
        # self.logger.info("[ClientStub] responseHandler recv response id:", id, ", apiId:", apiId)
        future = self.__futureQueue.Get(id)
        if future is None:
            # self.logger.error("[ClientStub] get future from queue error. id:", id)
            pass
        elif not future.Ready(response):
            self.logger.error("[ClientStub] set future ready error.")
