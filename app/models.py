from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


class User(BaseModel, UserMixin, db.Model):
    """用户"""
    __tablename__ = "blog_user"

    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    nick_name = db.Column(db.String(32), unique=True, nullable=False)  # 用户昵称
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码
    mobile = db.Column(db.String(11), unique=True, nullable=False)  # 手机号
    avatar_url = db.Column(db.String(256))  # 用户头像路径
    last_login = db.Column(db.DateTime, default=datetime.now)  # 最后一次登录时间
    is_admin = db.Column(db.Boolean, default=False)
    signature = db.Column(db.String(512))  # 用户签名
    gender = db.Column(  # 用户性别
        db.Enum(
            "MAN",  # 男
            "WOMAN"  # 女
        ),
        default="MAN")

    # 当前用户所发布的博客
    blogs_list = db.relationship('Blogs', backref='user', lazy='dynamic')

    def to_dict(self):  # 对一些模型数据进行格式化处理(封装展示效果)
        resp_dict = {
            "id": self.id,
            "nick_name": self.nick_name,
            "avatar_url": '127.0.0.1:5000/' + self.avatar_url if self.avatar_url else "",
            "mobile": self.mobile,
            "gender": self.gender if self.gender else "MAN",
            "signature": self.signature if self.signature else "",
            "news_count": self.blogs_list.count()
        }
        return resp_dict

    def to_admin_dict(self):
        resp_dict = {
            "id": self.id,
            "nick_name": self.nick_name,
            "mobile": self.mobile,
            "register": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "last_login": self.last_login.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return resp_dict

    @property
    def password(self):
        raise AttributeError("该属性是计算性属性, 不能直接取值")

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def check_password(self, password):  # 封装密码校验过程
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
###加载用户的回调函数接收以Unicode字符串形式表示的用户标示符
###如果能找到用户，这个函数必须返回用户对象，否则返回None。
def load_user(user_id):
    return User.query.get(int(user_id))


class Blogs(BaseModel, db.Model):
    """博客"""
    __tablename__ = "blog_blogs"

    id = db.Column(db.Integer, primary_key=True)  # 博客编号
    image_url = db.Column(db.String(256))  # 博客图片路径
    title = db.Column(db.String(256), nullable=False)  # 博客标题
    digest = db.Column(db.String(512), nullable=False)  # 博客摘要
    content = db.Column(db.Text, nullable=False)  # 博客内容
    clicks = db.Column(db.Integer, default=0)  # 浏览量
    category_id = db.Column(db.Integer, db.ForeignKey("blog_category.id"))  # 当前博客分类
    user_id = db.Column(db.Integer, db.ForeignKey("blog_user.id"))  # 当前博客的作者id

    def to_review_dict(self):
        resp_dict = {
            "id": self.id,
            "title": self.title,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return resp_dict

    def to_basic_dict(self):
        resp_dict = {
            "id": self.id,
            "title": self.title,
            "digest": self.digest,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "clicks": self.clicks,
            "image_url": self.index_image_url,
        }
        return resp_dict

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "title": self.title,
            "digest": self.digest,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "content": self.content,
            "image_url": self.image_url,
            "clicks": self.clicks,
            "category": self.category.to_dict(),
            "author": self.user.to_dict() if self.user else None
        }
        return resp_dict


class Category(BaseModel, db.Model):
    """新闻分类"""
    __tablename__ = "blog_category"

    id = db.Column(db.Integer, primary_key=True)  # 分类编号
    name = db.Column(db.String(64), nullable=False)  # 分类名
    news_list = db.relationship('Blogs', backref='category', lazy='dynamic')

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "name": self.name
        }
        return resp_dict
