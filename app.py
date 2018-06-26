import os
import sys

from flask import Flask
from flask import render_template, request

sys.path.append(os.path.join(os.path.dirname(__file__), "../genomics-ansible"))
import yaml_backend

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', d_word="Dumb")


@app.route('/available-packages', methods=['GET', 'POST'])
def available_packages():
    packages = yaml_backend.load_packages("/Users/dash/Documents/dash/genomics-ansible/role_definitions")

    if request.method == 'POST':
        selected_packages = request.form.getlist('package_checkbox')
        username = request.form.getlist('username')
        server_address = request.form.getlist('server_ip')
        for package in selected_packages:
            install_package.install_package(packages, package, username, server_address)

    return render_template('package_list.html', packages=packages)


if __name__ == '__main__':
    app.run()
