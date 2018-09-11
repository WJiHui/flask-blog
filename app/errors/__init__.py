# encoding:utf-8
# app/errors/__init__py


from flask import Blueprint

bp = Blueprint('errors', __name__, template_folder='templates')

from app.errors import handlers

