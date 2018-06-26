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
    if request.method == 'POST':
        print(request.form.getlist('package_checkbox'))

    packages = yaml_backend.load_packages("/Users/dash/Documents/dash/genomics-ansible/role_definitions")
    return render_template('package_list.html', packages=packages)


if __name__ == '__main__':
    app.run()
