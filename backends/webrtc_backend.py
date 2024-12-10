import asyncio
import json
import logging
import threading
import time
import numpy as np
import cv2
from queue import Queue
from go2_webrtc_driver.webrtc_driver import Go2WebRTCConnection, WebRTCConnectionMethod
from go2_webrtc_driver.constants import RTC_TOPIC, SPORT_CMD
from aiortc import MediaStreamTrack

logging.basicConfig(level=logging.FATAL)

class WebRTCBackend:
    def __init__(self):
        self.name = "WebRTC"
        self.conn = Go2WebRTCConnection(WebRTCConnectionMethod.LocalAP)
        self.frame_queue = Queue()
        print("Initializing WebRTC backend...")

    async def connect(self):
        await self.conn.connect()

    def initialize(self):
        audio_client = WebRTCAudio(self.conn)
        video_client = WebRTCVideo(self.conn, self.frame_queue)
        motion_client = WebRTCMotion(self.conn)
        telemetry_client = WebRTCTelemetry(self.conn)

        actions = {
            "Stand Up": motion_client.stand_up,
            "Lay Down": motion_client.lay_down,
            "Wave": motion_client.wave,
            "Heart": motion_client.heart,
            "Sit": motion_client.sit
        }

        return {
            "audio": audio_client,
            "video": video_client,
            "motion": motion_client,
            "telemetry": telemetry_client,
            "actions": actions
        }


class WebRTCAudio:
    def __init__(self, conn):
        self.conn = conn

    def play_sound(self, sound_name):
        print(f"Playing sound {sound_name} using WebRTC")

    def stop_sound(self):
        print("Stopping sound using WebRTC")

    def change_volume(self, volume):
        print(f"Changing volume to {volume} using WebRTC")


class WebRTCVideo:
    def __init__(self, conn: Go2WebRTCConnection, frame_queue: Queue):
        self.conn = conn
        self.frame_queue = frame_queue

    async def recv_camera_stream(self, track: MediaStreamTrack):
        while True:
            frame = await track.recv()
            img = frame.to_ndarray(format="bgr24")
            self.frame_queue.put(img)

    def start_video_stream(self):
        async def setup():
            try:
                await self.conn.connect()
                self.conn.video.switchVideoChannel(True)
                self.conn.video.add_track_callback(self.recv_camera_stream)
            except Exception as e:
                logging.error(f"Error in video stream: {e}")

        loop = asyncio.new_event_loop()
        threading.Thread(target=self.run_async_loop, args=(loop, setup)).start()

    def run_async_loop(self, loop: asyncio.AbstractEventLoop, setup: function):
        asyncio.set_event_loop(loop)
        
        loop.run_until_complete(setup())
        loop.run_forever()

    def stream_video(self):
        while True:
            if not self.frame_queue.empty():
                img = self.frame_queue.get()
                _, buffer = cv2.imencode('.jpg', img)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


class WebRTCMotion:
    def __init__(self, conn: Go2WebRTCConnection):
        self.conn = conn

    async def stand_up(self):
        await self.conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"], {"api_id": SPORT_CMD["StandUp"]}
        )

    async def lay_down(self):
        await self.conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"], {"api_id": SPORT_CMD["LayDown"]}
        )

    async def wave(self):
        await self.conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"], {"api_id": SPORT_CMD["Hello"]}
        )

    async def heart(self):
        await self.conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"], {"api_id": SPORT_CMD["Heart"]}
        )

    async def sit(self):
        await self.conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"], {"api_id": SPORT_CMD["Sit"]}
        )


class WebRTCTelemetry:
    def __init__(self, conn: Go2WebRTCConnection):
        self.conn = conn
        self.dog_data = {}

    async def fetch_telemetry(self):
        while True:
            response = await self.conn.datachannel.pub_sub.publish_request_new(
                RTC_TOPIC["TELEMETRY"], {"api_id": 2001}
            )

            if response['data']['header']['status']['code'] == 0:
                telemetry_data = json.loads(response['data']['data'])
                self.dog_data.update({
                    "voltage": format(telemetry_data.get("voltage", 0), ".2f"),
                    "current": format(telemetry_data.get("current", 0), ".2f"),
                    "temperature": format(telemetry_data.get("temperature", 0), ".2f"),
                    "velocity_x": format(telemetry_data.get("velocity_x", 0), ".2f"),
                    "velocity_y": format(telemetry_data.get("velocity_y", 0), ".2f"),
                    "yaw_speed": format(telemetry_data.get("yaw_speed", 0), ".2f")
                })
            await asyncio.sleep(1)

    def stream_data(self):
        while True:
            data_array = [
                {'name': 'Voltage', 'value': self.dog_data.get('voltage', 'N/A')},
                {'name': 'Current', 'value': self.dog_data.get('current', 'N/A')},
                {'name': 'Temperature', 'value': self.dog_data.get('temperature', 'N/A')},
                {'name': 'Velocity X', 'value': self.dog_data.get('velocity_x', 'N/A')},
                {'name': 'Velocity Y', 'value': self.dog_data.get('velocity_y', 'N/A')},
                {'name': 'Yaw Speed', 'value': self.dog_data.get('yaw_speed', 'N/A')}
            ]
            yield f"data: {json.dumps(data_array)}\n\n"
            time.sleep(0.1)

