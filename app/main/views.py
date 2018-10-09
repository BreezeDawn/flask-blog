from flask import send_from_directory, render_template, current_app, session, request, abort
from werkzeug.utils import secure_filename

from app.models import User, Blogs, Category
from fdfs_client.client import Fdfs_client
from . import main_blu


@main_blu.route('/')
def index():
    """首页"""
    page = request.args.get('page', 1, type=int)
    # 获取用户
    user_id = session.get('user_id')
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except BaseException as e:
            current_app.logger.error(e)
    user = user.to_dict() if user else None

    # 获取blog
    try:
        pagination = Blogs.query.order_by(Blogs.update_time.desc()).paginate(page,10)
    except BaseException as e:
        return abort(404)
    blogs = [blog.to_dict() for blog in pagination.items]
    return render_template('index.html', user=user, blogs=blogs,pagination=pagination)


@main_blu.route('/blog/<int:id>')
def blog(id):
    """文章详情页"""
    try:
        blog = Blogs.query.get(id)
    except BaseException as e:
        return abort(404)
    blog = blog.to_dict()
    return render_template('blog.html', blog=blog)


@main_blu.route('/postblog')
def postblog():
    """发表文章页"""
    return render_template('postblog.html')

@main_blu.route('/postimg',methods=['GET','POST'])
def postimg():
    """发表文章页"""
    if request.method == 'POST':
        # 获取文件对象
        file = request.files['imageFile']

        # 检查文件对象是否存在，且文件名合法
        if not file or not allowed_file(file.filename):
            return 'Upload Failed'  # 文件不合法

        # 去除文件名中不合法的内容
        filename = secure_filename(file.filename)

        # 将文件保存在fastdfs文件系统
        client = Fdfs_client(r"C:\Users\Maifeel\Desktop\项目\flask-blog\app\utils\fastdfs\client.conf")
        ret = client.upload_by_buffer(file.read())
        print(ret)
        return 'Upload Successfully'

    return render_template('postimg.html')

@main_blu.route('/category/<int:id>')
def category(id):
    """分类页"""
    try:
        category = Category.query.get(id)
    except BaseException as e:
        return abort(404)
    category = category.to_dict()
    return render_template('category.html', category=category)

@main_blu.route('/favicon.ico')
def favicon():
    return send_from_directory('static/image', 'favicon.ico')


# 设置允许上传的文件类型
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg'])


# 检查文件类型是否合法
def allowed_file(filename):
    # 判断文件的扩展名是否在配置项ALLOWED_EXTENSIONS中
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS