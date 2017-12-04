1. 数据库模型
	a. 直接增加一个follower表  app/models.py
		followers = db.Table('followers',
							db.Column('fans_id', db.Integer, db.ForeignKey('user.id')),
							db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
							)
		一共两列，一列是关注者的id，一个是被关注者的id,都是外键
	b. users 表中定义一个多对多的关系	app/models.py
		class User(db.Model, UserMixin):
			id = db.Column(db.Integer, primary_key=True)
			nickname = db.Column(db.String(64), index=True, unique=True)
			email = db.Column(db.String(64), index=True, unique=True)
			posts = db.relationship('Post', backref='author', lazy='dynamic')
			about_me = db.Column(db.String(140))
			last_seen = db.Column(db.String(20))
			followed_users = db.relationship('User',
									   secondary=followers,
									   primaryjoin=(followers.c.fans_id == id),
									   secondaryjoin=(followers.c.followed_id == id),
									   backref=db.backref('followers', lazy='dynamic'),
									   lazy='dynamic'
									  )

		‘User’ 是这种关系中的右边的表(实体)(左边的表/实体是父类)。因为定义一个自我指向的关系，我们在两边使用同样的类。
		secondary 指明了用于这种关系的辅助表。
		primaryjoin 表示辅助表中连接左边实体(发起关注的用户)的条件。注意因为 followers 表不是一个模式，获得字段名的语法有些怪异。
		secondaryjoin 表示辅助表中连接右边实体(被关注的用户)的条件。
		backref 定义这种关系将如何从右边实体进行访问。当我们做出一个名为 followed 的查询的时候，将会返回所有跟左边实体联系的右边的用户。当我们做出一个名为 followers 的查询的时候，将会返回一个所有跟右边联系的左边的用户。lazy 指明了查询的模式。dynamic 模式表示直到有特定的请求才会运行查询，这是对性能有很好的考虑。
		lazy 是与 backref 中的同样名称的参数作用是类似的，但是这个是应用于常规查询。
	
	c. 迁移一下  ./db_migrate.py
	    如果迁移出现暂时解决不了的问题， 例如改了字段的类型导致迁移失败的，删除数据库重新迁移
		from app import db       db.drop_all()
	

2. 添加和移除关注者
		class User(db.Model):
			#...
			def follow(self, user):
				if not self.is_following(user):
					self.followed_users.append(user)
					return self

			def unfollow(self, user):
				if self.is_following(user):
					self.followed_users.remove(user)
					return self

			def is_following(self, user):
				return self.followed_users.filter(followers.c.followed_id == user.id).count() > 0
				
		follow() 关注函数 首先是user没有关注本用户，然后加入到关注本用户的表中并返回本用户;否则返回None
		unfollow() 取关函数 首先是user已经关注本用户，然后从关注本用户的表中删除user并返回本用户;否则返回None
		follow()和unfollow()当返回一个用户对象的时候，这个对象必须被添加到数据库并且提交，这里其实是提交到follower表。
		is_following 方法在一行代码中做了很多。我们做了一个 followed 关系查询，这个查询返回所有当前用户作为关注者的 (follower, followed) 对。
                      count方法计算对数，如果有关注应该是1，最后返回一个bool型。

3. 测试
	class TestCase(unittest.TestCase):
		def test_follow(self):
			u1 = User(nickname='john', email='john@example.com')
			u2 = User(nickname='susan', email='susan@example.com')
			db.session.add(u1)
			db.session.add(u2)
			db.session.commit()
			assert u1.unfollow(u2) == None    # u1没有关注u2,直接返回None

			u = u1.follow(u2)
			db.session.add(u)
			db.session.commit()
			assert u1.is_following(u2)             # 1>0，返回True
			assert u1.followed_users.count() == 1  
			assert u1.followed_users.first().nickname == 'susan'
			assert u2.followers.count() == 1       
			assert u2.followers.first().nickname == 'john'
			print(u1.followed_users.all())               # u1关注的人
			print(u2.followers.all())                    # u2的粉丝
			
			u = u1.unfollow(u2)              # u1之前关注了u2,取关有效，返回u1
			assert u is not None
			db.session.add(u)
			db.session.commit()
			assert not u1.is_following(u2)   # u1没有关注u2
			assert u1.followed_users.count() == 0
			assert u2.followers.count() == 0

4. 数据库查询
	class User(db.Model, UserMixin):
		def followed_posts(self):
			return Post.query.join(followers,(followers.c.followed_id==Post.user_id))\
					.filter(followers.c.fans_id==self.id)\
					.order_by(Post.timestamp.desc())

	 Post 表中调用了 join 操作。这里有两个参数，第一个是其它的表，我们的 followers 表。第二参数就是连接的条件。		
	 连接操作所做的就是创建一个数据来自于 Post 和 followers 表的临时新的表，根据给定条件进行整合。
	from app.models import User, Post
	class TestCase(unittest.TestCase):
		def test_follow_post(self):
			u1 = User(nickname='john', email='john@example.com')
			u2 = User(nickname='susan', email='susan@example.com')
			u3 = User(nickname='wjh', email='wjh@example.com')
			db.session.add(u1)
			db.session.add(u2)
			db.session.add(u3)
			import datetime
			nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			p1 = Post(body='post from john', author=u1, timestamp=nowtime)
			p2 = Post(body='post from susan', author=u2, timestamp=nowtime)
			p3 = Post(body='post from wjh', author=u3, timestamp=nowtime)
			db.session.add(p1)
			db.session.add(p2)
			db.session.add(p3)
			db.session.commit()

			f1 = u1.follow(u2)
			f2 = u1.follow(u3)
			f3 = u2.follow(u1)
			f4 = u2.follow(u3)
			f5 = u3.follow(u1)
			f6 = u3.follow(u2)

			db.session.add(f1)
			db.session.add(f2)
			db.session.add(f3)
			db.session.add(f4)
			db.session.add(f5)
			db.session.add(f6)
			db.session.commit()

			# print(u1.followers.count())
			# print(dir(u1.followed_users))
			# print(u1.followed_users.all())
			print(u1.followed_posts().all())

 
 5. 用户关注自己 ，现在我们在注册的时候关注，跟原教程不同 view.py
	def register():
		newuser = User(nickname=nickname, email=email, about_me=about_me)
		db.session.add(newuser)
		db.session.add(user.follow(user))  # 增加
		db.session.commit()
	
	
6. 关注和取关的视图函数 view.py

		@app.route('/follow/<nickname>')
		@login_required
		def follow(nickname):
			user = User.query.filter_by(nickname=nickname).first()
			if user is None:
				flash('User %s not found' % nickname)
				return redirect(url_for('index'))
			if user == g.user:
				flash('You can not follow yourself.')
				return redirect(url_for('index'), nickname=nickname)
			u = g.user.follow(user)
			if u is None:
				flash("Cannot follow %s." % nickname)
				return redirect(url_for('user', nickname=nickname))
			db.session.add(u)
			db.session.commit()
			flash('You are now following %s.' % nickname)
			return redirect(url_for('user', nickname=nickname))

		@app.route('/unfollow/<nickname>')
		@login_required
		def unfollow(nickname):
			user = User.query.filter_by(nickname=nickname).first()
			if user is None:
				flash('User %s not found.' % nickname)
				return redirect(url_for('index'))
			if user == g.user:
				flash("You can't unfollow youself.")
				return redirect(url_for('user', nickname=nickname))
			u = g.user.unfollow(user)
			if u is None:
				flash("Can't unfollow %s." % nickname)
				return redirect(url_for('user', nickname=nickname))
			db.session.add(u)
			db.session.commit()
			flash('You have stopped unfollowing %s.' % nickname)
			return redirect(url_for('user', nickname=nickname))

		
		
		
7. app/templates/user.html 
	 a. 修改模板 ./app/templates/user.html
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

						<p>{{user.followers.count()}} followers |
						{% if user.id == g.user.id%}
							<p><a href="{{ url_for('edit') }}">Edit your profile.</a></p>
						{% elif not g.user.is_following(user) %}
							<a href="{{url_for('follow', nickname=user.nickname)}}">Follow</a>
						{% else %}
							<a href="{{url_for('unfollow', nickname=user.nickname)}}">UnFollow</a>
						{% endif %}
						</p>
					</td>
				</tr>
			</table>
			<hr>
			{% for post in posts %}
				{% include 'post.html' %}
			{% endfor %}
		{% endblock %}
	
	 b. 为了显示当前登录的用户，修改base.html中的一行
      <div>{{g.user.nickname}} blog: <a href="{{ url_for('index') }}">Home</a>
    
重启后测试一下,记住每次修改都要重启再测试。