数据库存储utc时间， 客户端使用js根据市区转化为本地时间

1. 下载https://github.com/miguelgrinberg/microblog/blob/master/app/static/js/moment.min.js
    放在自己的目录下 app/static/js/moment.min.js
	
2. 使用js/moment.min.js   
	app/templates/base.html:
	<script src="/static/js/moment.min.js"></script>

3. 
	./app/momentjs.py
		from jinja2 import Markup

		class momentjs(object):
			def __init__(self, timestamp):
				self.timestamp = timestamp

			def render(self, format):   # 注意这里我们前面已经把时间格式化了
				# return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))
				return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>"
							  % (self.timestamp, format))

			def format(self, fmt):
				return self.render("format(\"%s\")" % fmt)

			def calendar(self):
				return self.render("calendar()")

			def fromNow(self):
				return self.render("fromNow()")
				
	告诉 Jinja2 导入我们的类作为所有模板的一个全局变量
	app/__init__.py
		from .momentjs import momentjs
		app.jinja_env.globals['momentjs'] = momentjs

4. 保证存储的数据也是UTC时间
	def index(page=1):
		now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		改为
		now_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

	def before_request():	 
		g.user.last_seen = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		改为
		g.user.last_seen = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
		
5. 修改模板使用
	./app/templates/post.html		
		<td><i>{{ post.author.nickname }} says:   {{ momentjs(post.timestamp).format('YYYY-MM-DD HH:mm:ss') }}</i>
	./app/templates/user.html
		 <p><i>Last seen is:{{ momentjs(user.last_seen).calendar() }}</i></p>
	其他模式：
	fromNow()	5 years ago
	calendar()	01/01/2013