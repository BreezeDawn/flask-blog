import datetime
import random

from flask import send_from_directory, render_template, request, jsonify, current_app, session

from app import sr, db
from app.models import User
from app.response_code import RET, error_map
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


@main_blu.route('/register', methods=['POST'])
def register():
    # 接收数据
    username = request.json.get('username')
    password = request.json.get('password')
    mobile = request.json.get('mobile')

    # 校验数据
    if not all([username, password, mobile]):
        return jsonify(errno=RET.PARAMERR, errmsg=error_map[RET.PARAMERR])

    # 根据用户名从数据库中取出对应的记录
    try:
        user = User.query.filter_by(nick_name=username).first()
        user2 = User.query.filter_by(mobile=mobile).first()
    except BaseException as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])

    # 判断该用户是否存在
    if user or user2:  # 提示用户已存在
        return jsonify(errno=RET.DATAEXIST, errmsg=error_map[RET.DATAEXIST])

    user = User()
    user.nick_name = username
    user.password_hash = password
    user.mobile = mobile
    user.last_login = datetime.datetime.now()
    try:
        db.session.add(user)
        db.session.commit()
    except BaseException as e:
        current_app.logger.error(e)
        db.session.rollback()  # 设置回滚
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])

    # 状态保持  免密码登录
    session["user_id"] = user.id

    return jsonify(errno=RET.OK, errmsg=error_map[RET.OK])


@main_blu.route('/get_phone_idcode', methods=['POST'])
def get_phone_idcode():
    mobile = request.json.get('mobile')
    idCode = ''.join([str(x + random.randint(0, 9)) for x in [0, 0, 0, 0]])

    if sr.exists(mobile):
        sr.delete(mobile)

    try:
        sr.set("phone_idcode" + mobile, idCode, 60)
    except BaseException as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])

    current_app.logger.info("短信验证码为: %s" % idCode)
    return jsonify(errno=RET.OK, errmsg=error_map[RET.OK], idCode=idCode)


@main_blu.route('/favicon.ico')
def favicon():
    return send_from_directory('static/image', 'favicon.ico')
