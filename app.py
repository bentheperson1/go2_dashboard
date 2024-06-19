import subprocess
import os
import sys
import time
import json
import threading
import cv2
import numpy as np
from pathlib import Path

from flask import Flask, Response, render_template, redirect, url_for, jsonify, request

from unitree_sdk2py.idl.idl_dataclass import IDLDataClass
from unitree_sdk2py.core.dds.channel import DDSChannelFactoryInitialize
from unitree_sdk2py.utils.logger import setup_logging
from unitree_sdk2py.sdk.sdk import create_standard_sdk
from unitree_sdk2py.go2.audiohub.audiohub_client import AudioHubClient
from unitree_sdk2py.go2.video.video_client import VideoClient
from unitree_sdk2py.go2.sport.sport_client import SportClient

from werkzeug.utils import secure_filename

from dotenv import load_dotenv

from pydub import AudioSegment

load_dotenv(sys.path[0])

app = Flask(__name__, static_folder="static")
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.config['UPLOAD_FOLDER'] = 'sounds'
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'ogg', 'aac', 'flac'}

script_process = {'process': None, 'name': None}
dog_data = {}

idl_data_class = IDLDataClass()

SportModeState_ = idl_data_class.get_data_class('SportModeState_')
LowState_ = idl_data_class.get_data_class('LowState_')

move_speed = 0.5
turn_speed = 1

def LowStateHandler(msg: LowState_):
	dog_data["voltage"] = format(msg.power_v, ".2f")
	dog_data["current"] = format(msg.power_a, ".2f")
	dog_data["avg temp"] = round((msg.temperature_ntc1 + msg.temperature_ntc2) / 2)

def HighStateHandler(msg: SportModeState_):
	dog_data["velocity x"] = format(msg.velocity[0], ".2f")
	dog_data["velocity y"] = format(msg.velocity[1], ".2f")
	dog_data["velocity z"] = format(msg.velocity[2], ".2f")
	dog_data["yaw spd"] = format(msg.yaw_speed, ".2f")

setup_logging(verbose=True)

sdk = create_standard_sdk('UnitreeGo2SDK')
communicator = DDSChannelFactoryInitialize(domainId=0)
robot = sdk.create_robot(communicator, serialNumber='B42D2000XXXXXXXX')

low_state_sub = communicator.ChannelSubscriber("rt/lowstate", LowState_)
low_state_sub.Init(LowStateHandler, 10)

high_state_sub = communicator.ChannelSubscriber("rt/sportmodestate", SportModeState_)
high_state_sub.Init(HighStateHandler, 10)

audio_client: AudioHubClient = robot.ensure_client(AudioHubClient.default_service_name)
audio_client.SetTimeout(3.0)
audio_client.Init()

video_client: VideoClient = robot.ensure_client(VideoClient.default_service_name)
video_client.SetTimeout(3.0)
video_client.Init()

sport_client: SportClient = robot.ensure_client(SportClient.default_service_name)
sport_client.SetTimeout(3.0)
sport_client.Init()

actions_dict = {
	"Stand Up": sport_client.StandUp,
	"Lay Down": sport_client.StandDown,
	"Wave": sport_client.Hello,
	"Heart": sport_client.Heart,
	"Sit": sport_client.Sit
}

@app.route('/', methods=['GET', 'POST'])
def dashboard():
	try:
		scripts_directory = os.listdir(os.path.join(os.getcwd(), "scripts"))
		sounds_directory = os.listdir(os.path.join(os.getcwd(), "sounds"))

		active_script = script_process['name'] if script_process['name'] else 'None'
		return render_template('index.html', scripts=scripts_directory, actions=actions_dict.keys(), sounds=sounds_directory, dog_data=dog_data, active_script=active_script)
	except Exception as e:
		return str(e)

@app.route('/run_action/<action_name>')
def run_action(action_name):
	if action_name in actions_dict:
		threading.Thread(target=actions_dict[action_name]).start()
	
	return redirect(url_for('dashboard'))

@app.route('/update_joystick', methods=['POST'])
def update_joystick():
	data = request.get_json()

	x, y, yaw = 0, 0, 0

	if data['stickId'] == 'stick1':
		x = -data['y'] * move_speed
		y = -data['x'] * move_speed
	
	if data['stickId'] == 'stick2':
		yaw = -data['x'] * turn_speed

	sport_client.Move(x, y, yaw)

	return jsonify({'status': 'success', 'data': data}), 200

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		if 'file' not in request.files:
			return redirect(url_for('dashboard'))
		
		file = request.files['file']

		if file.filename == '':
			return redirect(url_for('dashboard'))
		
		if file and allowed_file(file.filename):
			filename = file.filename
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(request.url)
		
	return redirect(url_for('dashboard'))

def gen_frames():
	code, data = video_client.GetImageSample()

	while code == 0:
		code, data = video_client.GetImageSample()

		image_data = np.frombuffer(bytes(data), dtype=np.uint8)
		
		if image_data is None:
			continue

		frame = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

		ret, buffer = cv2.imencode('.jpg', frame)
		if not ret:
			continue

		frame_bytes = buffer.tobytes()
		yield (b'--frame\r\n'
			b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
	return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_data():
	while True:
		data_array = [
			{'name': 'Voltage', 'value': dog_data['voltage']},
			{'name': 'Current', 'value': dog_data['current']},
			{'name': 'Average Temp', 'value': dog_data['avg temp']},
			{'name': 'Velocity X', 'value': dog_data['velocity x']},
			{'name': 'Velocity Y', 'value': dog_data['velocity y']},
			{'name': 'Velocity Z', 'value': dog_data['velocity z']},
			{'name': 'Yaw Speed', 'value': dog_data['yaw spd']},
		]

		yield f"data: {json.dumps(data_array)}\n\n"
		
		time.sleep(0.1)

@app.route('/data')
def stream_data():
	return Response(generate_data(), mimetype='text/event-stream')

@app.route('/run/<script_name>')
def run_script(script_name):
	if '..' in script_name or '/' in script_name:
		return "Invalid script name."

	script_path = Path.cwd() / 'scripts' / script_name
	if not script_path.exists() or not script_path.is_file():
		return "Script not found."

	if script_process.get('process') is not None:
		stop_script()

	try:
		threading.Thread(target=lambda: run_script_thread(script_path, script_name)).start()
	except Exception as e:
		error_message = f"Error starting script {script_name}: {e}"
		return error_message

	return redirect(url_for('dashboard'))

def run_script_thread(script_path, script_name):
	try:
		process = subprocess.Popen([sys.executable, str(script_path)], text=True)
		script_process['process'] = process
		script_process['name'] = script_name

		process.wait()

		script_process['process'] = None
		script_process['name'] = None
	except Exception as e:
		script_process['process'] = None
		script_process['name'] = None

@app.route('/stop_script')
def stop_script():
	if script_process['process']:
		script_process['process'].terminate()
		script_process['process'].wait()
		script_process['process'] = None
		script_process['name'] = None
		print("Script stopped successfully")
	return redirect(url_for('dashboard'))

def audio_thread(sound_name):
	audio_client.MegaphoneEnter()
	audio_client.MegaphoneUpload(f"sounds/{sound_name}")

	time.sleep(AudioSegment.from_file(f"sounds/{sound_name}").duration_seconds)
	
	audio_client.MegaphoneExit()

@app.route('/play_sound/<sound_name>')
def play_sound(sound_name):
	threading.Thread(target=audio_thread, args=[sound_name]).start()

	return redirect(url_for('dashboard'))

@app.route('/delete_sound/<sound_name>')
def delete_sound(sound_name):
	filename = secure_filename(sound_name)
	file_path = os.path.join('sounds', filename)
	
	if os.path.exists(file_path):
		os.remove(file_path)

	return redirect(url_for('dashboard'))

@app.route('/stop_sound')
def stop_sound():
	audio_client.MegaphoneExit()

	return redirect(url_for('dashboard'))

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
