import os
import sys
import subprocess
import threading
from pathlib import Path
import asyncio

from flask import Flask, Response, render_template, redirect, url_for, jsonify, request

from werkzeug.utils import secure_filename

from backends.backend_factory import BackendFactory

app = Flask(__name__, static_folder="static")
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.config['UPLOAD_FOLDER'] = 'sounds'
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'ogg', 'aac', 'flac'}

script_process = {'process': None, 'name': None}
dog_data = {}
current_volume = 0

backend = BackendFactory.load_backend("RTC")
backend_clients = backend.initialize() if backend.name == "DDS" else asyncio.run(backend.initialize())

def allowed_file(filename: str):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def dashboard():
	try:
		scripts_directory = os.listdir(os.path.join(os.getcwd(), "scripts"))
		sounds_directory = os.listdir(os.path.join(os.getcwd(), "sounds"))
		active_script = script_process['name'] if script_process['name'] else 'None'

		return render_template(
			'index.html', 
			scripts=scripts_directory, 
			actions=backend_clients['actions'].keys(), 
			sounds=sounds_directory, 
			dog_data=dog_data, 
			active_script=active_script, 
			volume=current_volume,
			backend_type=backend.name
		)
	except Exception as e:
		return str(e)

@app.route('/run_action/<action_name>')
def run_action(action_name):
	if action_name in backend_clients['actions']:
		threading.Thread(target=backend_clients['actions'][action_name]).start()
	
	return redirect(url_for('dashboard'))

@app.route('/update_joystick', methods=['POST'])
def update_joystick():
	data = request.get_json()
	backend_clients['motion'].update_joystick(data)
	
	return jsonify({'status': 'success', 'data': data}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
	if 'file' not in request.files:
		return redirect(url_for('dashboard'))
	
	file = request.files['file']
	if file.filename and allowed_file(file.filename):
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
	
	return redirect(url_for('dashboard'))

@app.route('/video_feed')
def video_feed():
	return Response(
		backend_clients['video'].stream_video(), 
		mimetype='multipart/x-mixed-replace; boundary=frame'
	)

@app.route('/data')
def stream_data():
	return Response(
		backend_clients['telemetry'].stream_data(), 
		mimetype='text/event-stream'
	)

@app.route('/run/<script_name>')
def run_script(script_name):
	script_path = Path.cwd() / 'scripts' / script_name
	if not script_path.exists() or not script_path.is_file():
		return "Script not found."

	if script_process['process']:
		stop_script()

	threading.Thread(target=lambda: run_script_thread(script_path, script_name)).start()

	return redirect(url_for('dashboard'))

def run_script_thread(script_path, script_name):
	try:
		process = subprocess.Popen([sys.executable, str(script_path)], text=True)
		script_process.update({'process': process, 'name': script_name})
		process.wait()
	finally:
		script_process.update({'process': None, 'name': None})

@app.route('/stop_script')
def stop_script():
	if script_process['process']:
		script_process['process'].terminate()
		script_process['process'].wait()
		script_process.update({'process': None, 'name': None})

	return redirect(url_for('dashboard'))

@app.route('/play_sound/<sound_name>')
def play_sound(sound_name):
	threading.Thread(target=backend_clients['audio'].play_sound, args=[sound_name]).start()

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
	backend_clients['audio'].stop_sound()

	return redirect(url_for('dashboard'))

@app.route('/change_volume/<volume_lvl>')
def change_volume(volume_lvl):
	global current_volume

	current_volume = int(volume_lvl)
	backend_clients['audio'].change_volume(current_volume)

	return redirect(url_for('dashboard'))

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
