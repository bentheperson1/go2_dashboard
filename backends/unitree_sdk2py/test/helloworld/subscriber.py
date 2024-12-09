import time

from unitree_sdk2py.core.dds.channel import ChannelSubscriber, ChannelFactoryInitialize
from helloworld import HelloWorld

ChannelFactoryInitialize()

sub = ChannelSubscriber("topic", HelloWorld)
sub.Init()

while True:
    msg = sub.Read()

    if msg is None:
        print("subscribe error.")
    else:
        print("subscribe success. msg:", msg)

pub.Close()