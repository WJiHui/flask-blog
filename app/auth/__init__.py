# encoding:utf-8
# app/auth/__init__.py


from flask import Blueprint

bp = Blueprint('auth', __name__, template_folder="templates")

from app.auth import views




