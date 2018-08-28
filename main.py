from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_session import Session
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from config import Config

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)

sr = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

Session(app)

manager = Manager(app)  # 脚本启动,在configurations里添加runserver -d

Migrate(app, db)  # 初始化迁移器
manager.add_command('mc', MigrateCommand)  # 添加迁移命令,terminal python3 main.py mc init


@app.route('/')
def index():
    sr.set('name', 'maimai')  # redis存储测试
    session['name'] = 'maimai'  # session存储测试,现在会存储到redis
    return 'hello'


if __name__ == '__main__':
    manager.run()
