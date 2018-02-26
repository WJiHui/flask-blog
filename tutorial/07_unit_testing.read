1. 关闭调试模式 run.py 
	#!flask/bin/python
	from app import app
	app.run(debug=False, host='0.0.0.0', port=5000)
	
	如果应用再报错就会显示500内部程序错误
	
2. Custom HTTP error handlers 定制http错误处理器（重启生效）
	a. 定义视图 app.view.py 
		@app.errorhandler(404)
		def not_found_error(error):
			return render_template('404.html'), 404

		@app.errorhandler(500)
		def internal_error(error):
			db.session.rollback()        # 为了防止数据的误操作，回滚一下
			return render_template('500.html'), 500
	
	b. 编写模板 app/template/404.html 和 app/template/500.html 
		{% extends "base.html" %}

		{% block content %}
		  <h1>File Not Found</h1>
		  <p><a href="{{ url_for('index') }}">Back</a></p>
		{% endblock %}



		{% extends "base.html" %}

		{% block content %}
		  <h1>An unexpected error has occurred</h1>
		  <p>The administrator has been notified. Sorry for the inconvenience!</p>
		  <p><a href="{{ url_for('index') }}">Back</a></p>
		{% endblock %}
	
3. 发送错误到邮件
	a. 配置一个邮件服务器 config.py 
		# mail server settings
		MAIL_SERVER = '0.0.0.0' # 如果是真实发送应该是smtp.qq.com smtp.163.com
		MAIL_PORT = 25
		MAIL_USERNAME = None
		MAIL_PASSWORD = None

		# administrator list 
		ADMINS = ['you@example.com'] # 发送的目标邮箱
		
		
		注意如果要使用真实的邮箱发送，MAIL_PASSWORD一般应该是授权码而不是登录密码
	b. 报错时发送邮件 app/__init__.py

		from config import basedir, ADMINS, MAIL_SERVER, MAIL_POST, MAIL_USERNAME,MAIL_PASSWORD
		if not app.debug:
			import logging
			from logging.handlers import SMTPHandler
			credentials = None
			if MAIL_USERNAME or MAIL_PASSWORD:
				credentials = (MAIL_USERNAME, MAIL_PASSWORD)
			mail_handler = SMTPHandler(mailhost=(MAIL_SERVER, MAIL_POST),
									   fromaddr='no-reply@' + MAIL_SERVER,
									   toaddrs=ADMINS,
									   subject='blog failure',
									   credentials=credentials,
									   secure=None)
			mail_handler.setLevel(logging.ERROR)
			app.logger.addHandler(mail_handler)

	c. 打开一个伪造的邮箱服务器
	   python -m smtpd -n -c DebuggingServer 0.0.0.0:25
		打开的这个页面接收邮件信息
	提交一个主页改nickname,要重复的，就会报错，然后显示一个邮件信息，不能真的发邮件。
	
	
4. 同时记录日志到文件 app/__init__.py
	if not app.debug:
		import logging
		from logging.handlers import RotatingFileHandler
		file_handler = RotatingFileHandler(filename='tmp/microblog.log', mode='a',maxBytes=1*1024*1024, backupCount=5)
		formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s [in %(pathname)s:%(lineno)s]')
		file_handler.setFormatter(formatter)
		file_handler.setLevel(logging.INFO)
		app.logger.setLevel(logging.INFO)
		app.logger.addHandler(file_handler)
		app.logger.info('microblog startup')
		
	RotatingFileHandler备份5个日志文件，每个日志文件最大1M
	file_handler.setLevel(logging.INFO)设置日志的级别，CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
										默认是warning,只有日志级别以上的信息才会打印和保存。
	app.logger.info('microblog startup') 这里就会打印到日志中

5. 修复bug: 关于提交一个已存在的nickname报错的问题duplication bug
	a. 注册用户的时候检查是否有这个用户，现在写一个注册用户的功能
	   1.先写一个注册用户的表单类 app/models.py  
			from wtforms.validators import DataRequired, Length, Email # 多了一个Email验证字段
			class RegisterForm(FlaskForm):
				nickname = StringField('nickname', validators=[DataRequired()])
				email = StringField('email', validators=[DataRequired(), Email()])
				about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
		
		2. 增加一个函数验证表单的nickname和email是否已注册 app/models.py 
		    原博客里是按照给的nickname如果已存在，nickname后面自动加1，不行就再加1。
			class User(db.Model, User.Mixin)
			@staticmethod
			def make_unique_nickname(nickname):
				if User.query.filter_by(nickname=nickname).first() is None:
					return True
				else:
					return False
		
		3. 编写注册的视图函数 app/view.py
			@app.route('/register', methods=['GET', 'POST'])
			def register():
				if g.user is not None and g.user.is_authenticated:
					return redirect(url_for('index'))
				register_form = RegisterForm()
				if register_form.validate_on_submit():
					nickname = register_form.nickname.data
					email = register_form.email.data
					user_unique = User.make_unique_nickname(nickname)
					if user_unique:
						email_unique = User.make_unique_emali(email)
						if email_unique:
							about_me = register_form.about_me.data
							newuser = User(nickname=nickname, email=email, about_me=about_me)
							db.session.add(newuser)
							db.session.commit()
							login_user(newuser)
							return redirect(request.args.get('next') or url_for('index'))
						else:
							register_form.email.errors.append('This email has been register')
					else:
						register_form.nickname.errors.append('This user has been register')
				return render_template('register.html', title='register', form=register_form)

		4. 注册页面的模板 ./app/templates/register.html
				{% extends 'base.html' %}
				{% block content %}
				<h1> 注册用户</h1>

				<form action='' method='post' name='register'>
					{{ form.hidden_tag() }}
					<p>
						注册用户名：{{ form.nickname(size=24) }}<br>
						{% for error in form.nickname.errors %}
							<span style='color:red;'>[{{ error }}]</span>
						{% endfor %}
					</p>
					<p>
						注册邮箱：    {{ form.email }}<br>
						{% for error in form.email.errors %}
							<span style='color:red;'>[{{ error }}]</span>
						{% endfor %}
					</p>
					<p>
						个人说明：<br>
						{{ form.about_me(cols=100, row=1, size=140) }} <br>
						{% for error in form.about_me.errors %}
							<span style='color:red;'>[{{ error }}]</span>
						{% endfor %}
					<p> <input type=submit value='确认注册'></p>
				</form>
				{% endblock %}

		5. 在sign in登录页面加上一个注册的链接。app/template/login.html
			<h1>Sign In     or     <a href='{{ url_for('register')}}'>Register</a></h1>

	b. edit页面编辑用户主页面的修改也要限制nickname的修改不重复
		修改Edit类，app/forms.py
		from app.models import User
		class EditForm(FlaskForm):
			nickname = StringField('nickname', validators=[DataRequired()])
			about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

			def __init__(self, original_nickname, *args, **kwargs):
				FlaskForm.__init__(self, *args, **kwargs)
				self.original_nickname = original_nickname        # 记录原来的nickname

			def validate(self):
				if not FlaskForm.validate(self):
					return False
				if self.nickname.data = self.original_nickname:   # 提交的nickname和原来的nickname如果相同，说明没有修改nickname
					return True
				user = User.query.filter_by(nickname=self.nickname.data).first()
				if user is None:
					return True
				self.nickname.errors.append('This nickname is already use')
				return False
		validate方法应该视图函数form.validate_on_submit()检查时调用。 
		validate_on_submit 最后return self.is_submitted() and self.validate()

		
		修改视图函数
		def edit():
			form = EditForm(g.user.nickname) 
			if form.validate_on_submit():
				.....
		
		修改Edit模板  ./app/templates/edit.html
			{% extends 'base.html'%}

			{% block content %}
				<h1>Edit Your Profile</h1>
				<form action="" method="post" name="edit">
					{{ form.hidden_tag() }}
					<table>
						<tr>
							<td>用户名:</td>
							<td>{{ form.nickname(size=24) }}
								{% for error in form.nickname.errors %}
									<br><span style="color: red;">[{{ error }}]</span>
								{% endfor %}
							</td>
						</tr>
						<tr>
							<td>个人签名:</td>
							<td>{{ form.about_me(cols=100, row=1) }}
								{% for error in form.about_me.errors %}
									<br><span style="color: red;">[{{ error }}]</span>
								{% endfor %}
							</td>
						</tr>
						<tr>
							<td></td>
							<td><input type="submit" value="Save Changes"></td>
						</tr>
					</table>
				</form>
			{% endblock %}

6. 单元测试框架 ./tests.py
			#!flask/bin/python
			import os
			import unittest

			from config import basedir
			from app import app, db
			from app.models import User


			class TestCase(unittest.TestCase):
				def setUp(self):
					app.config['TESTING'] = True
					app.config['WTF_CSRF_ENABLED'] = False
					app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +  os.path.join(basedir, 'test.db')
					self.app = app.test_client()
					db.create_all()

				def tearDown(self):
					db.session.remove()
					db.drop_all()

				def test_avatar(self):
					print("""test avatar""")
					u = User(nickname='john', email='john@example.com')
					avatar = u.avatar(128)
					excepted = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
					assert avatar[0:len(excepted)] == excepted

				def test_make_unique_nickname(self):
					print("""test make unique nickname""")
					u = User(nickname='john', email='john@example.com')
					db.session.add(u)
					db.session.commit()
					unique_nickname = User.make_unique_nickname('john1')
					assert unique_nickname == True

					unique_nickname = User.make_unique_nickname('john')
					assert unique_nickname == False

			if __name__ == '__main__':
				# unittest.main()
				TestSuite = unittest.TestSuite()
				TestSuite.addTest(TestCase('test_avatar'))
				TestSuite.addTest(TestCase('test_make_unique_nickname'))
				runner = unittest.TextTestRunner()
				runner.run(TestSuite)

			setUp自动执行， 执行成功， 那么无论runTest是否成功，tearDown方法都将被执行。
			unittest.main() 所有测试都将被运行。使用“-h”选项运行模块可以查看所有可用的选项
			                命令行执行python unittest.py tests.TestCase.test_avatar
			下面一种方法是加入到测试套件中执行