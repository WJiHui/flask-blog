增加一个监控系统的蓝图

编辑app/________init__py
    from app.system import bp as system_bp
    app.register_blueprint(system_bp)

mkdir -p app/system/templates

编辑app/system/_____init__.py
    # encoding:utf-8
    # app/system/__init__.py
    
    from flask import Blueprint
    
    bp = Blueprint('system', __name__, template_folder='templates')
    
    from app.system import views

编辑app/system/models.py


编辑app/system/views.py


