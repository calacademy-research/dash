import os
import string
import subprocess
import sys

import socketio
from flask import Flask
from flask import render_template, request, redirect, flash
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename

sys.path.append(os.path.join(os.path.dirname(__file__), "genomics-ansible"))
import yaml_backend

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = 'uploads/'

app.config['SECRET_KEY'] = 'hi'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', d_word="Dumb")


@app.route('/available-packages', methods=['GET', 'POST'])
def available_packages():
    packages = yaml_backend.load_packages(os.path.join(os.path.dirname(__file__), "genomics-ansible/role_definitions"))

    if request.method == 'POST':
        selected_packages = request.form.getlist('package_checkbox')
        # username = request.form.getlist('username')
        # server_address = request.form.getlist('server_ip')
        # for package in selected_packages:
        #     pass
        print(selected_packages)

    return render_template('package_list.html', packages=packages)


def send_server(run_string):
    global socketio
    print(run_string)
    no_errors = ''.join(filter(lambda x: x in string.printable, run_string))
    if socketio is not None:
        socketio.emit('run_log', no_errors)

    print("Emmtted:" + no_errors)


def run_process(arg_array, directory=None, server_echo=False):
    global socketio

    bin = arg_array[0]
    if socketio is not None:
        send_server('running ' + bin + "\n")
    # print("Executing script:" + arg_array)
    # pass universal_newlines=True so Carriage Return interpreted as newline
    try:
        if directory is None:
            p = subprocess.Popen(arg_array, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        else:
            p = subprocess.Popen(arg_array, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=directory,
                                 universal_newlines=True)

        results = ""
        stdout_lines = iter(p.stdout.readline, "")
        for line in stdout_lines:
            if server_echo:
                send_server(line)
            results += line
        # retcode = p.poll()
    except Exception as e:
        send_server("Run aborted due to error:  " + e.strerror)
        send_server("Current working directory: " + directory)
        send_server("Command:                   " + bin)
        if socketio is not None:
            socketio.emit('done', bin)
        raise Exception(e.strerror)
    if socketio is not None:
        socketio.emit('done', bin)
    return results


@app.route('/ls-template', methods=['GET'])
def ls_template():
    return render_template('/ls.html')


@app.route('/ls-program', methods=['GET'])
def ls_program():
    run_process(['ls'], None, True)
    return "done", 200


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "Upload Successful"
    return render_template('/upload.html')


if __name__ == '__main__':
    global socketio
    socketio = SocketIO(app, async_mode="threading")
    socketio.run(app, debug=True, use_reloader=False)
    # app.run()
