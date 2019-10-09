#### 1. 处理web表单，需要使用flask-wtf
    安装 flask/bin/pip install flask-wtf
	
#### 2.创建一个配置文件 config.py
``` python
# encoding:utf-8

# 激活跨站点请求伪造
CSRF_ENABLED = True
# 激活CSRF需要，创建令牌，验证表单
SECRET_KEY = 'You want embarrass me, fuck you'
```
读取配置文件app/__init__.py
``` python    
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from app import views
```
#### 3. 用户登录表单 ./app/form.py  	表单的域定义成类的变量
``` python
# encoding:utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
   openid = StringField('openid', validators=[DataRequired()])
   remeber_me = BooleanField('remeber_me', default=False)
```

		
#### 4. 表单模板
登陆的模板  app/templates/login.html
``` html
 {% extends 'base.html' %}
 {% block content %}
 <h1>Sign In</h1>   
 <form action="" method='post' name='login'>
     {{ form.hidden_tag() }}
     <p>            
	Please enter your OpenID: <br>
	{{ form.openid(size=80)}}<br>
	{% for error in form.openid.errors %}   <!--	加强字段验证 !-->
			<span style="color: red;">[{{ error }}]</span>
	{% endfor %}<br>
     </p>           
     <p>{{ form.remeber_me }}Remeber me</p>
     <p><input type='submit' value='Sign In'</p>
 </form>            
 {% endblock %}     
```                           
form.hidden_tag() 模板参数将被替换为一个隐藏字段，用来是实现在配置中激活的 CSRF 保护。
	                  如果你已经激活了 CSRF，这个字段需要出现在你所有的表单中。
                           
#### 5. 表单视图和接收表单数据   
``` python
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

from flask import flash, redirect
from .form import LoginForm
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
	    flash('Login requested for OpenID=' + form.openid.data + ' remeber me='\
		  + str(form.remeber_me.data))
	    return redirect('/index')
	return render_template('login.html', title='sign in', form=form)
```
a. validate_on_submit验证数据是否合法
b. flash函数 呈现给用户页面消息      
修改 ./app/templates/base.html，闪现消息给用户
``` html
<html>                 
  <head>               
	{% if title %}     
	<title>{{title}} - microblog</title>
	{% else %}         
	<title>microblog</title>
	{% endif %}        
  </head>              
  <body>               
	<div>Microblog: <a href="/index">Home</a></div>
	<hr>               
	{% with messages = get_flashed_messages() %}
	{% if messages %}  
	<ul>               
	{% for message in messages %}
		<li>{{ message }} </li>
	{% endfor %}       
	</ul>              
	{% endif %}        
	{% endwith %}      
	{% block content %}{% endblock %}
  </body>              
</html>                
```
