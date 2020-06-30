from flask import Flask, Response
import subprocess
import json

def run_bash(command):
	process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	output, error = process.communicate()
	return output, error

def run_bash_rest(command):
	output, error = run_bash(command)
	output = str(output) if output else ''
	error = str(error) if error else ''
	js = json.dumps({"output": output, "error": error})
	resp = Response(js, status=200, mimetype='application/json')
	return resp

def get_next_workspace():
	bash_result_str = subprocess.check_output(['wmctrl', '-d'])
	bash_result_list = bash_result_str.split(b'\n')[:-1]
	current_workspace = [b'*' in k for k in bash_result_list].index(True)
	total_workspaces = len(bash_result_list)
	if current_workspace + 1 == total_workspaces:
		next_workspace = 0
	else:
		next_workspace = current_workspace + 1
	return next_workspace

app = Flask(__name__)

@app.route('/turnon')
def turn_monitor_on():
	command = "vcgencmd display_power 1"
	return run_bash_rest(command)

@app.route('/turnoff')
def turn_monitor_off():
	command = "vcgencmd display_power 0"
	return run_bash_rest(command)

@app.route('/changeworkspace')
def change_work_space():
	command = f"wmctrl -s {get_next_workspace()}"
	return run_bash_rest(command)

if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0')
