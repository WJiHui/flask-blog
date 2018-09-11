#!flask/bin/python
# encoding:utf-8
import os
import dotenv 

# 加入当前目录下的.env文件

basedir = os.path.dirname(__file__)
dotenv.Dotenv(os.path.join(basedir, '.env'))

class Config(object):

    # 激活跨站点请求伪造    
    CSRF_ENABLED = True 

    # 激活CSRF需要，创建令牌，验证表单
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'You want embarrass me, fuck you'  

    # 数据库配置
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///'+os.path.join(basedir, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

    # email配置
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # administrator list
    ADMINS = [os.environ.get('ADMINS')] or ['xxx@163.com']

    # pagination
    POSTS_AVG_PAGE = 3

    # search database,whoosh索引的位置
    WHOOSH_BASE = os.path.join(basedir, 'search.db')
    MAX_SEARCH_RESULTS = 50

    # available languages
    LANGUAGES= ['en', 'es', 'zh']
