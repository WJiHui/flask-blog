要使用数据库 ，先安装 flask/bin/pip install flask-sqlalchemy
                      flask/bin/pip install sqlalchemy-migrate
1. 数据库配置 config.py
	import os
	basedir = os.path.abspath(os.path.dirname(__file__)
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') # 数据库文件的路径
	SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')         # 文件夹，SQLAlchemy-migrate 数据文件存储在这里
	SQLALCHEMY_TRACK_MODIFICATIONS = True  # 如果没有这个创建数据库的时候会报警告
	
	
2. 初始化数据库 初始化文件app/__init__.py 
	
   from flask import Flask
   # from flask_wtf.sqlalchemy import SQLAlchemy  # 淘汰
   from flask_sqlalchemy import SQLAlchemy
  
   app = Flask(__name__)
   app.config.from_object('config')
   db = SQLAlchemy(app)
  
   from app import views, models

3. 根据用户表设计模型  app/models.py
	
		from app import db

		class User(db.Model):
			id = db.Column(db.Integer, primary_key=True)
			nickname = db.Column(db.String(64), index=True, unique=True)
			email = db.Column(db.String(64), index=True, unique=True)
			posts = db.relationship('Post', backref='author', lazy='dynamic')

			def __repr__(self):
				return '<User %r>' % (self.nickname)

		class Post(db.Model):
			id = db.Column(db.Integer, primary_key = True)
			body = db.Column(db.String(140))
			timestamp = db.Column(db.DateTime)
			user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

			def __repr__(self):
				return '<Post %r>' % (self.body)
	User 类中 posts是被构建成一个 db.relationship 字段。对于一个一对多的关系，db.relationship 字段通常是定义在“一”这一边。
	Post 类，这是用来表示用户编写的 blog
	
4. 创建数据库  ./db_create.py 
		#!flask/bin/python
		from migrate.versioning import api
		from config import SQLALCHEMY_DATABASE_URI
		from config import SQLALCHEMY_MIGRATE_REPO
		from app import db
		import os.path
		db.create_all()
		if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
			api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
			api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		else:
			api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
	
	 如果当前文件夹下已经有app.db ，再次执行会报错：migrate.exceptions.DatabaseAlreadyControlledError
	 
5. 迁移数据库 ./db_migrate.py
	SQLAlchemy-migrate 迁移的方式就是比较数据库(在本例中从 app.db 中获取)与我们模型的结构(从文件 app/models.py 获取)。
	两者间的不同将会被记录成一个迁移脚本存放在迁移仓库中。

		#!flask/bin/python
		import imp
		from migrate.versioning import api
		from app import db
		from config import SQLALCHEMY_DATABASE_URI
		from config import SQLALCHEMY_MIGRATE_REPO

		v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
		tmp_module = imp.new_module('old_model')
		old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		exec(old_model, tmp_module.__dict__)
		script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
		open(migration, "wt").write(script)
		api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		print('New migration saved as ' + migration)
		print('Current database version: ' + str(v))

	执行./db_migrate.py，每次迁移都会产生一个新的数据库版本
	
6. 数据库的升级和回退
	---------./db_upgrade.py
			#!flask/bin/python
			from migrate.versioning import api
			from config import SQLALCHEMY_DATABASE_URI
			from config import SQLALCHEMY_MIGRATE_REPO
			api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
			v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
			print('Current database version: ' + str(v))
	每次迁移完都要执行一下./db_upgrade.py 升级数据库到最高版本
	
	---------db_downgrade.py
			#!flask/bin/python
			from migrate.versioning import api
			from config import SQLALCHEMY_DATABASE_URI
			from config import SQLALCHEMY_MIGRATE_REPO
			v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
			api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - 1)
			print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))
	回退数据库一个版本
	
7.  使用命令行操作数据库
	a.  flask/bin/python 进入python执行环境
		>>> from app import db, models
		>>> u = models.User(nickname='john', email='john@email.com')
		>>> db.session.add(u)
		>>> db.session.commit()
		>>> u = models.User(nickname='susan', email='susan@email.com')
		>>> db.session.add(u)
		>>> db.session.commit()
		>>> users = models.User.query.all()     # 查询所有的用户信息
		>>> print users
		[<User u'john'>, <User u'susan'>]
		>>> for u in users:
		...     print u.id,u.nickname
		...
		1 john
		2 susan
		
		>>> u = models.User.query.get(1)        # 根据id查询用户primary_key
		>>> print u
		<User u'john'>
	
		如果db.session.commit()写入出现错误：
		sqlalchemy.exc.InvalidRequestError: This Session's transaction has been rolled back due to a previous exception during flush.
		可以使用db.session.close()关闭当前的提交，修改数据重新提交一下
	
	b. 提交一篇 blog:
		>>> import datetime
		>>> u = models.User.query.get(1)
		>>> p = models.Post(body='my first post!', timestamp=datetime.datetime.utcnow(), author=u)
		>>> db.session.add(p)
		>>> db.session.commit()
	c. 熟悉数据的查询
	
		# get all posts from a user
		>>> u = models.User.query.get(1)
		>>> print u
		<User u'john'>
		>>> posts = u.posts.all()
		>>> print posts
		[<Post u'my first post!'>]

		# obtain author of each post
		>>> for p in posts:
		...     print p.id,p.author.nickname,p.body
		...
		1 john my first post!

		# a user that has no posts
		>>> u = models.User.query.get(2)
		>>> print u
		<User u'susan'>
		>>> print u.posts.all()
		[]

		# get all users in reverse alphabetical order
		>>> print models.User.query.order_by('nickname desc').all()
		[<User u'susan'>, <User u'john'>]
		>>>
	d. 清除刚创建的所有的数据
	
		>>> users = models.User.query.all()
		>>> for u in users:
		...     db.session.delete(u)
		...
		>>> posts = models.Post.query.all()
		>>> for p in posts:
		...     db.session.delete(p)
		...
		>>> db.session.commit()
	
