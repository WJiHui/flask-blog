# encoding:utf-8
# app/system/__init__.py

from flask import Blueprint

bp = Blueprint('system', __name__, template_folder='templates')

from app.system import views
