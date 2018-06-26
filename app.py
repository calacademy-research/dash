from flask import Flask
from flask import render_template, request
import sys

sys.path.append('/Users/dash/Documents/dash/genomics-ansible/')
import install_packages

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', d_word="Dumb")


@app.route('/available-packages', methods=['GET', 'POST'])
def available_packages():
    if request.method == 'POST':
        print(request.form.getlist('package_checkbox'))

    packages = install_packages.load_packages("/Users/dash/Documents/dash/genomics-ansible/role_definitions")
    return render_template('package_list.html', packages=packages)


if __name__ == '__main__':
    app.run()
