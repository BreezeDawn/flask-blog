from flask import send_from_directory, render_template, current_app, session

from app.models import User

from . import main_blu


@main_blu.route('/')
def index():
    user_id = session.get('user_id')
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except BaseException as e:
            current_app.logger.error(e)
    user = user.to_dict() if user else None
    return render_template('index.html', user=user)


@main_blu.route('/favicon.ico')
def favicon():
    return send_from_directory('static/image', 'favicon.ico')
