from flask import send_from_directory

from . import main_blu


@main_blu.route('/')
def index():
    return 'hello'


@main_blu.route('/favicon.ico')
def favicon():
    return send_from_directory('static/image', 'favicon.ico')
