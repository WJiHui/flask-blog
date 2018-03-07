把创建的数据库中的用户和blog融入到应用程序中去

1. 配置登录系统，app/__init__.py 
   需要用到两个扩展 Flask-Login 和 Flask-OpenID
		from flask import Flask
		from flask_sqlalchemy import SQLAlchemy
		import os
		from flask_login import LoginManager
		#from flask_openid import OpenID
		from config import basedir

		app = Flask(__name__)
		app.config.from_object('config')
		db = SQLAlchemy(app)

		lm = LoginManager()
		lm.init_app(app)
		#oid = OpenID(app, os.path.join(basedir, 'tmp'))


		from app import views, models


2. 重构用户模型 app/models.py 
	Flask-Login 扩展需要在我们的 User 类中实现一些特定的方法。

		class User(db.Model):
			id = db.Column(db.Integer, primary_key=True)
			nickname = db.Column(db.String(64), index=True, unique=True)
			email = db.Column(db.String(64), index=True, unique=True)
			posts = db.relationship('Post', backref='author', lazy='dynamic')

			def is_authenticated(self):
			     return True

			def is_actice(self):
		              return True

			def is_anonymous(self):
			     return False

			def get_id(self):
			     try:
			 	return unicode(self.id) # python2
			     except NameError:
				return str(self.id)     # python3

			def __repr__(self):
			     return '<User %r>' % (self.nickname)

3. user_loader 回调
    用于从数据库加载用户。这个函数将会被 Flask-Login 使用(文件 app/views.py)
		from flask import flash, redirect, session, url_for, request, g
		from flask_login import login_user, logout_user, current_user, login_required
		from app import app, db, lm, #oid
		from .models import User
		from .form import LoginForm

		@app.route('/login', methods=['GET', 'POST'])
		# @oid.loginhandler
		def login():
			if g.user is not None and g.user.is_authenticated():
			     return redirect(url_for('index'))
			form = LoginForm()
			if form.validate_on_submit():
			     session['remeber_me'] = form.remeber_me.data
			     return oid.try_login(form.openid, ask_for=['nickname', 'email'])
			return render_template('login.html', title='sign in', form=form)
	flask.g是一个全局变量，在一个请求周期中用来存储和共享数据。
	g.user 检查是否被设置成一个认证用户，如果是重定向到首页。就是已经登录的用户访问login函数时，返回首页
	flask.session 提供了一个更加复杂的服务对于存储和共享数据。
					一旦数据存储在会话对象中，在来自同一客户端的现在和任何以后的请求都是可用的。
	#oid.try_login 被调用是为了触发用户使用 Flask-OpenID 认证				
					
	如果在 next 页没有提供的情况下，我们会重定向到首页，否则会重定向到 next 页。				
 
	
	
4. Flask-Login 需要知道哪个视图允许用户登录。我们在应用程序模块初始化中配置(文件 app/__init__.py):
    lm = LoginManager()
    lm.init_app(app)
    lm.login_view = 'login'
	
5. 全局变量g  app/views.py 
		@app.before_request
		def before_request():
		      g.user = current_user
	任何使用了 before_request 装饰器的函数在接收请求之前都会运行
