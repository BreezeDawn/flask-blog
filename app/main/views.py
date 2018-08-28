from app import sr
from . import main_blu


@main_blu.route('/')
def index():
    sr.set('name', 'mai')  # 测试sr使用
    return 'hello'
