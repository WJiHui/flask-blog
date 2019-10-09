 1. 创建一个模板app/templates/base.html
 ``` html
		<html>
			<head>
				{% if title %}
				<title>{{title}} -- microblog</title>
				{% else %}
				<title>microblog</title>
				{% endif %}
			</head>
			<body>
				<div>Microblog: <a href='/index'>Home</a><div>
				<hr>
				{% block content %}{% endblock%}
			 </body>
		</html>
```				
 继承模板app/templates/index.html
		{% extends 'base.html'%}
		{% block content %}
			<h1>Hi,{{user.nickname}}!</h1>
		{% for post in posts%}
			<div><p>{{post.author.nickname}} says:{{post.body}}</p></div>
		{% endfor %}
		{% endblock %}

 2. 使用这个模板 app/view.py
	from flask import render_template
	from app import app

	@app.route('/')
	@app.route('/index')
	def index():
		user = {'nickname':'saisai'}
		posts = [
			{'author': {'nickname': 'John'}, 'body': 'Beautiful day in Portland'},
			{'author': {'nickname': 'Susa'}, 'body': 'The Avengers movie was cool'},
		]
		return render_template('index.html', title='Home', user=user, posts=posts)
