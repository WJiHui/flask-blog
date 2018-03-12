# encoding:utf-8

# 激活跨站点请求伪造
CSRF_ENABLED = True 

# 激活CSRF需要，创建令牌，验证表单
SECRET_KEY = 'You want embarrass me, fuck you'  

import os
SQLALCHEMY_TRACK_MODIFICATIONS = True
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# email server 
MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = '15856932005@163.com'
MAIL_PASSWORD = 'xxxxx'

# administrator list
ADMINS = ['15856932005@163.com']


# pagination
POSTS_AVG_PAGE = 3

# search database
WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 50

# available languages
LANGUAGES= ['en', 'es', 'zh']
