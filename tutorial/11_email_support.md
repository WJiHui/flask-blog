原文是用户关注了另外一个用户的时候，就会向这个用户发送一个邮件

1. 修改邮箱配置 
   a. config.py
		# email server
		MAIL_SERVER = 'smtp.163.com'
		MAIL_PORT = 465
		MAIL_USE_TLS = False
		MAIL_USE_SSL = True
		MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
		MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

		# administrator list
		ADMINS = ['15856932005@163.com']


	   说明：
	   MAIL_SERVER 是邮件服务器，qq是smpt.qq.com，google是smtp.googlemail.com
	   TLS   传输层安全性 Transport Layer Security
	   SSL  （TLS前身）安全套接层 Secure Sockets Layer，这两个默认都是False
	   MAIL_PORT   注意这里是MAIL_PORT，把__init__.py 里的两个MAIL_POST也改成MAIL_PORT
             	   邮箱端口，一般情况下都是25，如果打开 MAIL_USE_SSL,那么端口改为465
	   MAIL_USERNAME 和 MAIL_PASSWORD 可以直接写入源代码，但是这样不安全，可以使用环境变量的方式
					命令行输入 export MAIL_USERNAME=xxx@163.com 和  export MAIL_PASSWORD=xxx
					可以检查一下 echo $MAIL_USERNAME  和 echo $MAIL_PASSWORD
					这里需要注意的是邮箱密码不是登录密码，而是授权码，需要到登录到邮件，在邮箱设置里设置
		ADMINS      第一个是作为发件方，应该和MAIL_USERNAME一致（这是按照下面测试部分的代码写的，后面可以改）。
		            后面是收件方，可以是多个，如果只填写一个就是自己发给自己
	
	b. 初始化一个Mail对象 app/__init__.py
	   放在 lm.login_view = 'login'这一行的下面
		from flask_mail import Mail
		mail = Mail(app)
		
	c. 测试发送邮件 ./test_send_email.py		
			#!flask/bin/python
			from flask_mail import Message
			from app import app, mail
			from config import ADMINS
			msg = Message('test subject', sender=ADMINS[0], recipients=ADMINS)
			msg.body = 'text body'
			msg.html = '<b>HTML</b> body'
			with app.app_context():
					mail.send(msg)
		这里在命令行也可以执行，建议写成脚本形式，方便多次调试。
		发送邮件的内容有两种格式，纯文本和html格式，两种都写的话，会看客户端接收设置，一般会优先html格式的邮件
	
	注意，如果用的是os.environ.get()方式获取用户名和密码，则下次登录需要重新export设置，否则会报下面的错误
	smtplib.SMTPSenderRefused: (553, 'authentication is required,163 smtp1,C9GowAAnYPxEfBtaQeFDAA。。。)

2.  A simple email framework 简单的邮件框架
	a. 专门发送邮件的函数  ./app/emails.py
	b. 关注提醒，发送邮件
	 
	# encoding:utf-8

	from flask_mail import Message,Mail
	from app import app
	from flask import render_template
	from config import ADMINS
	mail = Mail(app)

	def send_email(subject, sender, recipients, text_body, html_body):
		msg = Message(subject, sender=sender, recipients=recipients)
		msg.body = text_body
		msg.html = html_body
		mail.send(msg)

	def follower_notification(followed, follower):
		send_email("[microblog] %s is now following you!" % follower.nickname,
					ADMINS[0],
					[followed.email],
					render_template("follower_email.txt",
									user=followed, follower=follower),
					render_template("follower_email.html",
									user=followed, follower=follower)
				  )
				  
	c. 两个发送模板
		./app/templates/follower_email.txt
			Dear [{{ user.name }}],
				{{ follower.nickname }} is now a follower. Click on the following link to visit {{ follower.nickname }}'s profile page:
				{{ url_for('user', nickname=follower.nickname, _external=True) }}
			Regards,
				The microblog admin
			
		./app/templates/follower_email.html
			<p>Dear {{ user.nickname }},</p>
			<p><a href='{{ url_for('user', nickname=follower.nickname, _external=True) }}'>{{ follower.nickname }}</a>is now a follower.</p>
			<table>
				<tr valign='top'>
					<td> <img src="{{ follower.avatar(50) }}"</td>
					<td> <a href="{{ url_for('user', nickname=follower.nickname, _external=True) }}">{{ follower.nickname }}</a><br/>{{ follower.about_me }}</td>
				</tr>
			</table>
			<p>Regards,</p>
			<p>The <code> mircroblog</code> </p>

		url_for 有 _external = True 参数，这个参数是保证生成的url会包括域名
	
	d. 整合到视图函数 app/views.py
		from .emails import follower_notification

		@app.route('/follow/<nickname>')
		@login_required
		def follow(nickname):
			...
			flash('You are now following %s.' % nickname)
			follower_notification(user, g.user)
			return redirect(url_for('user', nickname=nickname))

		
	e. 为了更好的测试，希望能够容易看到关注的人，在user.html加了一个功能
		{% if user.last_seen %}
			<p><i>Last seen is:{{ user.last_seen }}</i></p>
		{% endif %}
		<p>My email: <i>{{ user.email }}</i></p>
		<p>{{user.followers.count()}} followers
			{% for follower in user.followers %}
				<p><a href="{{url_for('user', nickname=follower.nickname)}}">{{ follower.nickname }}</a></p>
			{% endfor %}

	建立两个使用邮箱注册的用户，互相关注发送邮件。

	
3. Asynchronous 异步调用  
    上面关注之后有一个几秒的缓冲，这是因为Flask-Mail是同步的synchronous，发送邮件时阻塞了
	./app/emails.py
		# encoding:utf-8

		from flask_mail import Message,Mail
		from app import app
		from flask import render_template
		from .decorators import async
		from config import ADMINS
		mail = Mail(app)

		@async
		def send_async_email(app, msg):
			with app.app_context():
				mail.send(msg)

		def send_email(subject, sender, recipients, text_body, html_body):
			msg = Message(subject, sender=sender, recipients=recipients)
			msg.body = text_body
			msg.html = html_body
			send_async_email(app, msg)

	./app/decorators.py
		from threading import Thread

		def async(f):
			def wrapper(*args, **kwargs):
				thr = Thread(target=f, args=args, kwargs=kwargs)
				thr.start()
			return wrapper

	
4. 还可以发送附件和批量发送等 http://python.jobbole.com/86765/