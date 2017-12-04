创建一个专门的数据库用于全文搜索，使用 Whoosh扩展，注意在python3上有兼容问题 

安装	flask/bin/pip install Flask-WhooshAlchemy

1.  配置数据库  config.py

	# search database
	WHOOSH_BASE = os.path.join(basedir, 'search.db')

2. 修改模型，给数据建立搜索引擎  app/models.py 
	import sys
	from app import app
	
	class Post(db.Model):
		__searchable__ == ['body']  # add


	if sys.version_info < (3,0):
		import flask_whooshalchemy
		flask_whooshalchemy.whoosh_index(app, Post)

3. 删除全部的posts
	flask/bin/python
	>>> from app.models import Post
	>>> from app import db
	>>> for post in Post.query.all():
	...    db.session.delete(post)
	>>> db.session.commit()
	
4. 在应用中实现搜索
    a. 打开博客，创建一个用户，写三个博客。
	    my first post
		my second post
		my third and last post
	
	b. 返回搜索结果的最大数量  config.py
	    MAX_SEARCH_RESULTS = 50
	
	c. 定义搜索表单 
	
	d. 修改搜索模板，加入搜索框，只有认证过的用户登录后才能查询
		./app/templates/base.html
        <div>{{g.user.nickname}} blog: <a href="{{ url_for('index') }}">Home</a>
            {% if g.user.is_authenticated %}
                <a href="{{ url_for('user', nickname=g.user.nickname) }}">Your Profile</a>
                <form style="display: inline;" action="{{ url_for('search') }}"  method="post" name="search">
                    {{ g.search_form.hidden_tag() }}
                    {{ g.search_form.search(size=20) }}
                    <input type="submit" value="Search">
                </form>
            |   <a href="{{ url_for('logout') }}">Logout</a>
            {% endif %}
        </div>

		./app/views.py
		from .form import LoginForm, RegisterForm, PostForm, SearchForm

		@app.before_request
		def before_request():
			g.user = current_user
			if g.user.is_authenticated:
				g.user.last_seen = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				db.session.add(g.user)
				db.session.commit()
				g.search_form = SearchForm()
			

	
	e. 搜索的视图函数 ./app/views.py 
		@app.route('/search', methods=['POST'])
		@login_required
		def search():
			if not g.search_form.validate_on_submit():
				return redirect(url_for('index'))
			return redirect(url_for('search_results', query=g.search_form.search.data))

		from config import POSTS_AVG_PAGE, MAX_SEARCH_RESULTS
		@app.route('/search_results/<query>')
		@login_required
		def search_results(query):
			results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
			return render_template('search_results.html', query=query, results=results)

	f. 搜索结果的模板
		./app/templates/post.html
		<table border='1'>
			<tr valign='top'>
				<td><img src="{{ post.author.avatar(20) }}"></td>  # 修改
				<td><i>{{ post.author.nickname }} says:</i>
					<br> <b> {{ post.body }}</b>
				</td>
			</tr>
		</table>
		
		./app/templates/search_results.html
		{% extends 'base.html' %}

		{% block content %}
		<h1> Search results for "{{ query }}"</h1>
		{% for post in results %}
			{% include 'post.html' %}
		{% endfor %}
		{% endblock %}

	