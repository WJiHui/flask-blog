# encoding:utf-8

from flask_mail import Message 
from flask import render_template, current_app
from app.decorators import async 
from app import mail 

# from multiprocessing import Pool 
# def do_send_email(app, msg):
    # with app.app_context():
        # mail.send(msg) 


# class SendEmail(object):
    # def __init__(self, app, msg):
        # self.app = app
        # self.msg = msg
        # self.p = Pool(5)  
    # def async_run(self):
        # self.p.apply_async(func=do_send_email, args=(self.app, self.msg))
        # self.p.close()
        # self.p.join()

# def send_async_email(app, msg):
    # foo = SendEmail(app, msg)
    # foo.async_run()


@async  
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(current_app._get_object_object(), msg)

def follower_notification(followed, follower):
    send_email("[microblog] %s is now following you!" % follower.nickname,
                current_app.config.get['ADMINS'][0],
                [followed.email],
                render_template("follower_email.txt", 
                                user=followed, follower=follower),
                render_template("follower_email.html", 
                                user=followed, follower=follower)
              )


