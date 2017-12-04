#!flask/bin/python
from flask_mail import Message
from app import app, mail
from config import ADMINS
msg = Message('test subject', sender=ADMINS[0], recipients=ADMINS)
msg.html = '<b>HTML</b> body'
msg.body = 'text body'
with app.app_context():
	mail.send(msg)

