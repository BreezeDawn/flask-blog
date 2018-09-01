from flask import send_from_directory, render_template, request

from . import main_blu


@main_blu.route('/')
def index():
    return render_template('index.html')

@main_blu.route('/get_phone_idcode',methods=['POST'])
def get_phone_idcode():
    data = request.form.get()
    print(data)


@main_blu.route('/favicon.ico')
def favicon():
    return send_from_directory('static/image', 'favicon.ico')
