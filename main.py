from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis


class Config:
    # app.config
    DEBUG = True

    # sqlalchemy.config
    SQLALCHEMY_DATABASE_URI = "mysql://root:xiaodianchi@127.0.0.1:3306/flask_blog"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否追踪数据库变化

    # redis.config
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = '6379'


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
sr = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)


@app.route('/')
def index():
    sr.set('name', 'maimai')  # redis存储测试
    return 'hello'


if __name__ == '__main__':
    app.run()
