1. 定义一个用户的主页 app/view.py
	
	@app.route('/user/<nickname>')
	@login_required
	def user(nickname):
		user = User.query.filter_by(nickname=nickname).first()
		if user is None:
			flash('User %s not found' % nickname)
			return redirect(url_for('index'))
		posts = Post.query.filter_by(user_id=user.id)
		return render_template('user.html', user=user, posts=posts)
2. 在主页中显示更多的信息
	a.增加两个User类字段 和 头像显示函数
		class User(db.Model, UserMixin):
			id = db.Column(db.Integer, primary_key=True)
			nickname = db.Column(db.String(64), index=True, unique=True)
			email = db.Column(db.String(64), index=True, unique=True)
			posts = db.relationship('Post', backref='author', lazy='dynamic')
			about_me = db.Column(db.String(140))
			last_seen = db.Column(db.String(20))
			
			def avatar(self, size):
				return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' %\
			(md5(self.email.encode('utf-8')).hexdigest(), size)

	b.增加字段完需要进行一次迁移使修改生效 ./do_migrate.py
	
	c. 显示头像，头像依靠Gravatar服务提供用户的头像，这个要先去注册
		d=mm 表示如果这个用户没有注册，返回一个默认的头像。这里的头像存在盗用的可能

	d. 如何写入last_seen    app/view.py 
		def before_request():
			g.user = current_user
			if g.user.is_authenticated:
				 g.user.last_seen = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				 db.session.add(g.user)   # 更新操作
				 db.session.commit() 	
	e.如何写入read_me信息，新增一个用户的表单
		1.先定义一个表单  app/form.py
			# encoding:utf-8

			from flask_wtf import FlaskForm
			from wtforms import StringField, BooleanField, TextAreaField
			from wtforms.validators import DataRequired, Length

			class EditForm(FlaskForm):
				nickname = StringField('nickname', validators=[DataRequired()])
				about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
				
		2. 编辑read_me页面的模板   ./app/templates/edit.html
				{% extends 'base.html'%}

				{% block content %}
					<h1>Edit Your Profile</h1>
					<form action="" method="post" name="edit">
						{{ form.hidden_tag() }}
						<table>
							<tr>
								<td>Your nickname:</td>
								<td>{{ form.nickname(size=24) }}</td>
							</tr>
							<tr>
								<td>About Yourself:</td>
								<td>{{ form.about_me(cols=100, row=1) }}</td>
									{% for error in form.about_me.errors %}
										<!--<br> <p>{{error}}</p>-->
										<br><span style="color: red;">[{{ error }}]</span>
									{% endfor %}
							</tr>
							<tr>
								<td></td>
								<td><input type="submit" value="Save Changes"></td>
							</tr>
						</table>
					</form>
				{% endblock %}

		3. 编辑好模板后，编写视图函数  ./app/views.py

				from .form import LoginForm, EditForm
				@app.route('/edit', methods=['GET', 'POST'])
				@login_required
				def edit():
					form = EditForm()
					if form.validate_on_submit():
						g.user.nickname = form.nickname.data
						g.user.about_me = form.about_me.data
						db.session.add(g.user)
						db.session.commit()
						flash('Your changes has been saved.')
						return redirect(url_for('user', nickname=g.user.nickname))
					else:
						print('g.user')
						form.nickname.data = g.user.nickname
						form.about_me.data = g.user.about_me
						return render_template('edit.html', form=form)

		4.  在用户主页加上编辑read_me的链接
		
3. 显示用户的主页  
	a. 修改导航栏 app/templates/base.html， 显示出用户主页的链接
        <div>Microblog: <a href="{{ url_for('index') }}">Home</a>
            {% if g.user.is_authenticated %}
              <a href="{{ url_for('user', nickname=g.user.nickname) }}">Your
                  Profile</a>
            | <a href="{{ url_for('logout') }}">Logout</a>
            {% endif %}
        </div>
	a. 显示用户主页app/templates/user.html

		{% extends "base.html" %}

		{% block content %}
			<table border='1'>
				<tr valign="top">
					<td><img src="{{ user.avatar(128) }}"></td>
					<td>
						<h1>User:{{ user.nickname }}</h1>
						{% if user.about_me %}
							<p>About me:{{ user.about_me }}</p>
						{% endif %}
						{% if user.last_seen %}
							<p><i>Last seen is:{{ user.last_seen }}</i></p>
						{% endif %}
						{% if user.id == g.user.id%}
							<p><a href="{{ url_for('edit') }}">Edit</a></p>
						{% endif %}
					</td>
				</tr>
			</table>
			<hr>
			{% for post in posts %}
				{% include 'post.html' %}
			{% endfor %}
		{% endblock %}
		
	b. 单独定义一个app/templates/post.html模板用来显示blog.
		<table border='1'>
			<tr valign='top'>
				<td><img src="{{ user.avatar(20) }}"></td>
				<td><i>{{ post.author.nickname }} says:</i>
					<br> <b> {{ post.body }}</b>
				</td>
			</tr>
		</table>



