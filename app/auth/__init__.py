from flask import Blueprint

auth_blu = Blueprint('auth', __name__)

from .views import *