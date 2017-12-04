from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from flask_babel import Babel
babel = Babel(app)


from app import views, models
from flask_mail import Mail
mail = Mail(app)

from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME,MAIL_PASSWORD
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler(mailhost=(MAIL_SERVER, MAIL_PORT), 
                               fromaddr='no-reply@' + MAIL_SERVER, 
                               toaddrs=ADMINS, 
                               subject='blog failure',
                               credentials=credentials,
                               secure=None)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(filename='tmp/microblog.log', mode='a',maxBytes=1*1024*1024, backupCount=10)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s [in %(pathname)s:%(lineno)s]')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')

from .momentjs import momentjs
app.jinja_env.globals['momentjs'] = momentjs



