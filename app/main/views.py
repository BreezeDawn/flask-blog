from . import main_blu
import logging

@main_blu.route('/')
def index():
    logging.error('hahahha')
    return 'hello'
