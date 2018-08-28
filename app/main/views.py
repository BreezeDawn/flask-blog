from . import main_blu

@main_blu.route('/')
def index():
    return 'hello'
