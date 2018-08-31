from flask import send_from_directory, render_template

from . import main_blu


@main_blu.route('/')
def index():
    return render_template('index.html')


@main_blu.route('/favicon.ico')
def favicon():
    return send_from_directory('static/image', 'favicon.ico')
