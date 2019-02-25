import os
from flask_mail import Mail
from flask_babel import Babel
from flask_login import LoginManager
from flask_migrate import Migrate 
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask import request, Flask, current_app
from config import Config
from app.momentjs import Momentjs 


db = SQLAlchemy()
migrate = Migrate()
lm = LoginManager()
lm.login_view = 'auth.login'
mail = Mail()
babel = Babel()
moment = Moment()
bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.jinja_env.globals['Momentjs'] = Momentjs

    db.init_app(app)
    migrate.init_app(app)
    lm.init_app(app)
    mail.init_app(app)
    babel.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from app.system import bp as system_bp
    app.register_blueprint(system_bp)

    if not app.debug and not app.testing:
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            credentials = (app.config['MAIL_USERNAME'],
                           app.config['MAIL_PASSWORD'])
        mail_handler = SMTPHandler(
                    mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']), 
                    fromaddr='no-reply@' + app.config['MAIL_SERVER'], 
                    toaddrs=app.config['ADMINS'], 
                    subject='blog failure',
                    credentials=credentials,
                    secure=None)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if not app.debug and not app.testing:
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(filename='tmp/microblog.log', mode='a',maxBytes=1*1024*1024, backupCount=10)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s [in %(pathname)s:%(lineno)s]')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        app.logger.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('microblog startup')
    
    return app



@babel.localeselector 
def get_locale():
    languages = request.accept_languages.best_match(current_app.config['LANGUAGES'])
    return languages 



