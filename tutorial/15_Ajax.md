1. 使用ajax进行同步翻译
    a. 语言识别，使用语言识别库guess_language, 这里使用它的一个衍生版本,支持py2和py3
        pip install guess-language_spirit

    b. 在博客提交的时候就保存它的语言
        app/models.py
        class Post(db.Model):
            language = db.Column(db.String(5))
        修改数据库后需要迁移一下 ./db_migrate.py

        app/views.py
        from guess_language import guess_language 
        def index(page=1):
            if form.validate_on_submit():
                language = guess_language(form.post.data)
                if language == 'UNKNOW' or len(language)  > 5:
                    language = ''
                post = Post(body=form.post.data, timestamp=now_time,
                        author=g.user, language=language)
    
    c. 添加一个翻译的连接
        app/templates/post.html
            <td><img src="{{ post.author.avatar(20) }}"></td>
            <td>
            {% if post.language and post.language != g.locale %}
            <br><br>
                <a href="#">{{ _("Translate") }}</a>
            {% endif %}
        现在还没有给出具体的翻译连接

    d. 第三方翻译服务
        https://cloud.google.com/translate/docs/
        https://www.microsoft.com/en-us/translator/ 
        需要注册，要银行卡什么的，这章烂尾了。。。
