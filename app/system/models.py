# encoding:utf-8
from app import db


class Stat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(256))
    mem_free = db.Column(db.Integer)
    mem_usage = db.Column(db.Integer)
    mem_total = db.Column(db.Integer)
    load_avg = db.Column(db.String(128))
    time = db.Column(db.Integer)
