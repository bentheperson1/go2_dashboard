import time
import json
import numpy as np
import cv2

from unitree_sdk2py.sdk.sdk import create_standard_sdk
from unitree_sdk2py.idl.idl_dataclass import IDLDataClass
from unitree_sdk2py.core.dds.channel import DDSChannelFactoryInitialize, DDSCommunicator

from unitree_sdk2py.go2.audiohub.audiohub_client import AudioHubClient
from unitree_sdk2py.go2.video.video_client import VideoClient
from unitree_sdk2py.go2.sport.sport_client import SportClient
from unitree_sdk2py.go2.vui.vui_client import VuiClient

class DDSBackend:
    def __init__(self):
        self.name = "DDS"
        self.idl_data_class = IDLDataClass()
        self.sdk = create_standard_sdk('UnitreeGo2SDK')
        self.communicator = DDSChannelFactoryInitialize(domainId=0)
        self.robot = self.sdk.create_robot(self.communicator, serialNumber='B42D2000XXXXXXXX')

    def initialize(self):
        audio_client: AudioHubClient = self.robot.ensure_client(AudioHubClient.default_service_name)
        video_client: VideoClient = self.robot.ensure_client(VideoClient.default_service_name)
        sport_client: SportClient = self.robot.ensure_client(SportClient.default_service_name)
        vui_client: VuiClient = self.robot.ensure_client(VuiClient.default_service_name)

        audio_client.Init()
        video_client.Init()
        sport_client.Init()
        vui_client.Init()

        actions = {
            "Stand Up": sport_client.RecoveryStand,
            "Lay Down": sport_client.StandDown,
            "Wave": sport_client.Hello,
            "Heart": sport_client.Heart,
            "Sit": sport_client.Sit
        }

        backend_clients = {
            "audio": DDSAudio(audio_client),
            "video": DDSVideo(video_client),
            "motion": DDSMotion(sport_client),
            "telemetry": DDSTelemetry(self.communicator, self.idl_data_class),
            "actions": actions
        }

        return self.sdk, self.robot, backend_clients


class DDSAudio:
    def __init__(self, audio_client_var: AudioHubClient, vui_client_var: VuiClient):
        self.audio_client = audio_client_var
        self.vui_client = vui_client_var

    def play_sound(self, sound_name):
        self.audio_client.MegaphoneEnter()
        self.audio_client.MegaphoneUpload(f"../sounds/{sound_name}")
    
    def stop_sound(self):
        self.audio_client.MegaphoneExit()

    def change_volume(self, volume):
        self.vui_client.SetVolume(volume)


class DDSVideo:
    def __init__(self, client: VideoClient):
        self.client = client

    def stream_video(self):
        while True:
            code, data = self.client.GetImageSample()

            if code == 0:
                image_data = np.frombuffer(bytes(data), dtype=np.uint8)
                frame = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

                _, buffer = cv2.imencode('.jpg', frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


class DDSMotion:
    def __init__(self, client: SportClient):
        self.client = client
        self.move_speed = 0.5
        self.turn_speed = 1.0

    def update_joystick(self, data):
        x, y, yaw = 0, 0, 0

        if data['stickId'] == 'stick1':
            x = -data['y'] * self.move_speed
            y = -data['x'] * self.move_speed

        if data['stickId'] == 'stick2':
            yaw = -data['x'] * self.turn_speed
            
        self.client.Move(x, y, yaw)


class DDSTelemetry:
    def __init__(self, communicator: DDSCommunicator, idl_data_class: IDLDataClass):
        self.dog_data = {}
        LowState_ = idl_data_class.get_data_class('LowState_')
        SportModeState_ = idl_data_class.get_data_class('SportModeState_')

        low_state_sub = communicator.ChannelSubscriber("rt/lowstate", LowState_)
        high_state_sub = communicator.ChannelSubscriber("rt/sportmodestate", SportModeState_)

        low_state_sub.Init(self.low_state_handler, 10)
        high_state_sub.Init(self.high_state_handler, 10)

    def low_state_handler(self, msg):
        self.dog_data.update({
            "voltage": format(msg.power_v, ".2f"),
            "current": format(msg.power_a, ".2f"),
            "avg temp": round((msg.temperature_ntc1 + msg.temperature_ntc2) / 2)
        })

    def high_state_handler(self, msg):
        self.dog_data.update({
            "velocity x": format(msg.velocity[0], ".2f"),
            "velocity y": format(msg.velocity[1], ".2f"),
            "velocity z": format(msg.velocity[2], ".2f"),
            "yaw spd": format(msg.yaw_speed, ".2f")
        })

    def stream_data(self):
        while True:
            data_array = [
                {'name': 'Voltage', 'value': self.dog_data.get('voltage', 'N/A')},
                {'name': 'Current', 'value': self.dog_data.get('current', 'N/A')},
                {'name': 'Average Temp', 'value': self.dog_data.get('avg temp', 'N/A')},
                {'name': 'Velocity X', 'value': self.dog_data.get('velocity x', 'N/A')},
                {'name': 'Velocity Y', 'value': self.dog_data.get('velocity y', 'N/A')},
                {'name': 'Velocity Z', 'value': self.dog_data.get('velocity z', 'N/A')},
                {'name': 'Yaw Speed', 'value': self.dog_data.get('yaw spd', 'N/A')}
            ]

            yield f"data: {json.dumps(data_array)}\n\n"
            time.sleep(0.1)
