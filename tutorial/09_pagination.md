分页管理

1. 博客提交
	a. 定义一个提交博客表单的表单类 app/forms.py
		class PostForm(FlaskForm):
			post = TextAreaField('post', validators=[DataRequired()])

	b. 在模板中使用表单      app/templates/index.html

		{% extends 'base.html'%}
		{% block content %}
			<h1>Hi,{{user.nickname}}! this is your blogs</h1>
			<form action="" method='post' name="post">
				{{ form.hidden_tag() }}
				<table>
					<tr>
						<td>Say something:</td>
						<td>{{ form.post(size=30,cols=100, maxlength=140) }}
							{% for error in form.post.errors %}
								<br><span style="color: red;">[{{ error }}]</span>
							{% endfor %}
						</td>
					</tr>
					<tr>
						<td></td>
						<td><input type='submit' value="Post!"></td>
					</tr>
				</table>
			</form>

		{% for post in posts%}
			<div><p>{{post.author.nickname}} says:{{post.body}}</p></div>
		{% endfor %}
		{% endblock %}

	c. 视图函数中向模板传入表单 app/views.py

		from .form import LoginForm, RegisterForm, PostForm

		@app.route('/', methods=['GET', "POST"])
		@app.route('/index', methods=['GET', 'POST'])
		@login_required
		def index():
			form = PostForm()
			if form.validate_on_submit():
				now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				post = Post(body=form.post.data, timestamp=now_time, author=g.user)
				db.session.add(post)
				db.session.commit()
				flash('Your post is now live')
				return redirect(url_for('index'))
			user = g.user
			posts = Post.query.filter_by(user_id=user.id)
			return render_template('index.html', title='Home', user=user, posts=posts, form=form)

 2. 显示自己关注的人的博客。
		 posts = Post.query.filter_by(user_id=user.id)
	改为 posts = user.followed_posts().all()
	因为自己首先会关注自己，所以也会看到自己的博客，按照时间顺序降序排序。
	
3.  分页： 按照上面的方法显示博客，如果数量太多全部显示，这样效率也太低。
	a.	posts = user.followed_posts().paginate(1, 3, False).items
		paginate 方法能够被任何查询调用。它接受三个参数:

		开始页数，一般从 1 开始，
		每一页的项目数，这里也就是说每一页显示的 blog 数，
		错误标志。如果是 True，当请求的范围页超出范围的话，一个 404 错误将会自动地返回到客户端的网页浏览器。如果是 False，返回一个空列表而不是错误。
    
	b. 把每页显示的项目数作为配置参数写入config.py 
		# pagination
		POSTS_PER_PAGE = 3	
	
	c. 根据url的页数来返回相应视图 
		默认   http://47.89.xxx.xx:5000/index/ 
		默认   http://47.89.xxx.xx:5000/index/1 
		第二页 http://47.89.xxx.xx:5000/index/2

		from config import POSTS_AVG_PAGE

		@app.route('/', methods=['GET', "POST"])
		@app.route('/index', methods=['GET', 'POST'])
		@app.route('/index/<int:page>',methods=['GET', 'POST'])
		@login_required
		def index(page=1):
			form = PostForm()
			if form.validate_on_submit():
				now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				post = Post(body=form.post.data, timestamp=now_time, author=g.user)
				db.session.add(post)
				db.session.commit()
				flash('Your post is now live')
				return redirect(url_for('index'))
			user = g.user
			posts = user.followed_posts().paginate(page, POSTS_AVG_PAGE, False).items
			return render_template('index.html', title='Home', user=user, posts=posts, form=form)

4. 分页导航
	a. 返回Pagination object   app/views.py
        posts = user.followed_posts().paginate(page, POSTS_AVG_PAGE, False)
    
	b. 在模板中使用pagination对象进行分页导航  app/templates/index.html

		{% for post in posts.items %}
			<!--<div><p>{{post.author.nickname}} says:{{post.body}}</p></div>-->
			{% include 'post.html' %}   
		{% endfor %}
		{% if posts.has_prev %}
			<a href="{{ url_for('index', page=posts.prev_num) }}">&lt;&lt;前一页</a>
		{% else %}&lt;&lt;前一页
		{% endif %}|
		{% if posts.has_next %}
			<a href="{{ url_for('index', page=posts.next_num) }}">后一页 &gt;&gt;</a>
		{% else %}后一页&gt;&gt;
		{% endif %}
		
		{% include 'post.html' %} 这里使用post.html子模板
		posts.has_prev            如果前一页存在返回True，否则返回False, posts.has_next类似
		{% else %}&lt;&lt;前一页  这一行可以有也可以没有
		
5. 用户信息页 
	a. 用户页的视图函数
		@app.route('/user/<nickname>')
		@app.route('/user/<nickname>/<int:page>')
		@login_required
		def user(nickname, page=1):
			user = User.query.filter_by(nickname=nickname).first()
			if user is None:
				flash('User %s not found' % nickname)
				return redirect(url_for('index'))
			posts = user.posts.paginate(page, POSTS_AVG_PAGE, False)
			return render_template('user.html', user=user, posts=posts)
			
	b. 用户视图的模板 修改./app/templates/user.html

			{% for post in posts.items %}
				{% include 'post.html' %}
			{% endfor %}
			{% if posts.has_prev %}<a href="{{ url_for('user', nickname=user.nickname, page=posts.prev_num) }}">&lt;&lt;前一页</a>
			{% else %}&lt;&lt;前一页
			{% endif %}
			{% if posts.has_next %}<a href="{{ url_for('user', nickname=user.nickname, page=posts.next_num) }}">后一页&gt;&gt;</a>
			{% else %}后一页&gt;&gt;
			{% endif %}
