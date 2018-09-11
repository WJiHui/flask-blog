#!flask/bin/python
# encoding:utf-8
"""
flask+gevent提高flask的并发能力
./flask/bin/pip install gevent 
"""
from gevent import monkey
from gevent.pywsgi import WSGIServer
from app import create_app 

monkey.patch_all()
app = create_app()
WSGIServer(('0.0.0.0', 5000), app).serve_forever()
