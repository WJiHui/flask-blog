https://github.com/miguelgrinberg/microblog
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
http://www.pythondoc.com/flask-mega-tutorial/index.html

# encoding : utf-8

# 1. 在flask_microblog文件夹下创建一个虚拟环境文件夹，命令为flask    
#    python3：python -m venv flask
#    python2: pip install virtualenv
#             安装完之后创建虚拟环境文件夹：virtualenv flask 
# 2. 虚拟环境创建完，现在安装flask应用，安装flask和flask扩展的命令如下，
#    windows上注意斜杠是相反的,路径是flask/Scripts/，而不是这里的flask/bin
#   flask/bin/pip install flask
#   flask/bin/pip install flask-login
#   flask/bin/pip install flask-openid
#   flask/bin/pip install flask-mail # 以下未装
#   flask/bin/pip install flask-sqlalchemy  数据库
#   flask/bin/pip install sqlalchemy-migrate  数据库迁移
#   flask/bin/pip install flask-whooshalchemy  全文搜索
#   flask/bin/pip install flask-wtf    
#   flask/bin/pip install flask-babel  语言转换
#   flask/bin/pip install guess_language
#   flask/bin/pip install flipflop
#   flask/bin/pip install coverage

# 3. 在flask_microblog文件夹下创建基本的文件结构
#   mkdir app
#   mkdir app/static
#   mkdir app/templates
#   mkdir tmp

# 4. 创建一个应用初始化脚本 app/__init__.py
    from flask import Flask

    app = Flask(__name__)
    from app import views

# 5. 接上上面编写试图模块 app/views.py
from app import app

@app.route('/')
@app.round('/index')
def index():
    return 'Hello World'


# 6. 主目录下编写run.py脚本，启动应用

#!flask/bin/python
from app import app
app.run(debug = True, host='0.0.0.0', port=5000)
    # 如果不写host，默认127.0.0.1，从外网可能访问不到
    # 然后执行run.py 应用启动 默认5000端口
