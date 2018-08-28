from flask import Flask
from redis import StrictRedis
from flask_session import Session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import config_dict


db = None   # type: SQLAlchemy
sr = None   # type: StrictRedis


def create_app(config_type):
    app = Flask(__name__)

    config_class = config_dict[config_type]
    app.config.from_object(config_class)

    global db, sr

    db = SQLAlchemy(app)

    sr = StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

    Session(app)

    Migrate(app, db)  # 初始化迁移器

    from app.main import main_blu
    app.register_blueprint(main_blu)

    return app
