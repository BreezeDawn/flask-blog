from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:xiaodianchi@127.0.0.1:3306/flask_blog"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否追踪数据库变化


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


@app.route('/')
def index():
    return 'hello'


if __name__ == '__main__':
    app.run()
