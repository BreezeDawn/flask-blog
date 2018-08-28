from datetime import timedelta

from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_session import Session


class Config:
    # app.config
    DEBUG = True

    # sqlalchemy.config
    SQLALCHEMY_DATABASE_URI = "mysql://root:xiaodianchi@127.0.0.1:3306/flask_blog"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否追踪数据库变化

    # redis.config
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = '6379'

    # session.config
    SESSION_TYPE = 'redis'  # session存储的数据库类型
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # session存储使用的redis对象,默认是Redis(),我们要使用StrictRedis
    SESSION_USE_SIGNER = True  # 是否对sessionID进行加密存储
    SECRET_KEY = '21cG0Z3SmdeqmPFn1gykFaTC+uSgBRx6LtmKJg6lFKAFH33zgSO9tpfE6Wtvnzvi'  # base64.b64encode(os.urandom(48))
    PERMANENT_SESSION_LIFETIME = timedelta(days=7) # session持久化存储时间,默认持久化存储31days

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)

sr = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

Session(app)


@app.route('/')
def index():
    sr.set('name', 'maimai')  # redis存储测试
    session['name'] = 'maimai' # session存储测试,现在会存储到redis
    return 'hello'


if __name__ == '__main__':
    app.run()
