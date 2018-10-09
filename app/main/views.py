from flask import send_from_directory, render_template, current_app, session, request, abort

from app.models import User, Blogs, Category

from . import main_blu


@main_blu.route('/')
def index():
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
    try:
        blog = Blogs.query.get(id)
    except BaseException as e:
        return abort(404)
    blog = blog.to_dict()
    return render_template('blog.html', blog=blog)

@main_blu.route('/category/<int:id>')
def category(id):
    try:
        category = Category.query.get(id)
    except BaseException as e:
        return abort(404)
    category = category.to_dict()
    return render_template('category.html', category=category)

@main_blu.route('/favicon.ico')
def favicon():
    return send_from_directory('static/image', 'favicon.ico')
