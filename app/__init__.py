import logging
from logging.handlers import RotatingFileHandler

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
    """"app初始化"""

    # 创建app对象
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

    # 开启日志
    setup_log()

    return app


def setup_log():
    """"日志设定"""

    # 设定日志的 监控等级
    logging.basicConfig(level=logging.DEBUG)

    # 定义日志记录格式
    formatter = logging.Formatter('%(levelname)s %(pathname)s:%(lineno)d  %(message)s')

    # 创建日志文件处理器,记得创建logs文件夹,且.gitignore中不应该忽略logs,但是需要忽略log
    # 且git不会管理空文件夹,因此需要中logs中创建一个隐藏文件保持logs不为空
    log_file_hanlder = RotatingFileHandler('logs/log', maxBytes=1024*1024*100, backupCount=10)

    # 为处理器设定记录格式
    log_file_hanlder.setFormatter(formatter)

    # 为全局日志增添日志文件处理器
    logging.getLogger().addHandler(log_file_hanlder)
