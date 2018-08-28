from flask import Blueprint

main_blu = Blueprint('main', __name__)

from .views import *
