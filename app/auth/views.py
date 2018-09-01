import random
from datetime import datetime

from flask import request, jsonify, current_app, session, redirect, url_for
from flask_login import login_required, login_user, logout_user

from app import db, sr
from app.models import User
from app.auth import auth_blu
from app.response_code import RET, error_map

@auth_blu.route('/login', methods=['POST'])
def login():
    # 获取数据
    username = request.json.get('username')
    password = request.json.get('password')
    # 校验数据
    if not all([username, password]):
        return jsonify(errno=RET.PARAMERR, errmsg=error_map[RET.PARAMERR])

    try:
        user = User.query.filter_by(nick_name=username).first()
        user2 = User.query.filter_by(mobile=username).first()
    except BaseException as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])

    if not user and not user2:
        return jsonify(errno=RET.USERERR, errmsg=error_map[RET.USERERR])

    user = user if not user2 else user2

    # 校验密码
    if not user.check_password(password):
        return jsonify(errno=RET.PWDERR, errmsg=error_map[RET.PWDERR])

    # 记录用户最后的登录时间
    user.last_login = datetime.now()

    # 状态保持
    login_user(user)

    # 将校验结果以json返回
    return jsonify(errno=RET.OK, errmsg=error_map[RET.OK])

@auth_blu.route('/register', methods=['POST'])
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
    if user:  # 提示用户已存在
        return jsonify(errno=RET.DATAEXIST, errmsg=u'该用户名已被注册')
    if user2:
        return jsonify(errno=RET.DATAEXIST, errmsg=u'该手机号已被注册')

    user = User()
    user.nick_name = username
    user.password = password
    user.mobile = mobile
    user.last_login = datetime.now()
    try:
        db.session.add(user)
        db.session.commit()
    except BaseException as e:
        current_app.logger.error(e)
        db.session.rollback()  # 设置回滚
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])

    # 状态保持  免密码登录
    login_user(user)

    return jsonify(errno=RET.OK, errmsg=error_map[RET.OK])


@auth_blu.route('/get_phone_idcode', methods=['POST'])
def get_phone_idcode():
    mobile = request.json.get('mobile')
    idCode = ''.join([str(x + random.randint(0, 9)) for x in [0, 0, 0, 0]])

    user = None
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except BaseException as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg=error_map(RET.DATAERR))
    if user:
        return jsonify(errno=RET.DATAEXIST, errmsg=u"该手机号已被注册")

    if sr.exists(mobile):
        sr.delete(mobile)

    try:
        sr.set("phone_idcode" + mobile, idCode, 60)
    except BaseException as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])

    current_app.logger.info("短信验证码为: %s" % idCode)
    return jsonify(errno=RET.OK, errmsg=error_map[RET.OK], idCode=idCode)


@auth_blu.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
