import time
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class WebRTCBackend:
    def __init__(self):
        self.name = "WebRTC"
        print("Initializing WebRTC backend...")

    def initialize(self):
        # Dummy setup for WebRTC mock functionality
        backend_clients = {
            "audio": WebRTCAudio(),
            "video": WebRTCVideo(),
            "motion": WebRTCMotion(),
            "telemetry": WebRTCTelemetry(),
            "actions": {
                "Stand Up": lambda: print("WebRTC: Standing up..."),
                "Lay Down": lambda: print("WebRTC: Laying down...")
            }
        }
        return None, None, backend_clients


class WebRTCAudio:
    def play_sound(self, sound_name):
        print(f"Playing sound {sound_name} using WebRTC")

    def stop_sound(self):
        print("Stopping sound using WebRTC")

    def change_volume(self, volume):
        print(f"Changing volume to {volume} using WebRTC")


class WebRTCVideo:
    def stream_video(self):
        while True:
            print("Streaming video using WebRTC...")
            time.sleep(1)
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + b"\r\n"


class WebRTCMotion:
    def update_joystick(self, data):
        print(f"Moving robot using WebRTC: {data}")


class WebRTCTelemetry:
    def stream_data(self):
        while True:
            mock_data = [
                {'name': 'Voltage', 'value': '12.5'},
                {'name': 'Current', 'value': '2.3'}
            ]
            yield f"data: {json.dumps(mock_data)}\n\n"
            time.sleep(1)
