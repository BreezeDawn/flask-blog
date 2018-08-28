from flask import Flask
from redis import StrictRedis
from flask_session import Session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import config_dict

# 数据库全局变量
db = None   # type: SQLAlchemy
sr = None   # type: StrictRedis


def create_app(config_type):
    # 初始化app对象
    app = Flask(__name__)

    # 获取传入环境对应的配置类,并进行配置设定
    config_class = config_dict[config_type]
    app.config.from_object(config_class)

    # 数据库全局设定
    global db, sr

    db = SQLAlchemy(app)

    sr = StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

    # Session设定
    Session(app)

    # 初始化迁移器
    Migrate(app, db)

    # 创建主蓝图
    from app.main import main_blu
    app.register_blueprint(main_blu)

    return app
