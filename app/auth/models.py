import sys
from hashlib import md5
from datetime import datetime
from app import db
from flask import current_app
from flask_login import UserMixin


followers = db.Table('followers', 
                    db.Column('fans_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                    )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed_users = db.relationship('User', 
                               secondary=followers,
                               primaryjoin=(followers.c.fans_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic'
                              )

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' %\
    (md5(self.email.encode('utf-8')).hexdigest(), size)

    def is_authenticated(self):
        return True

    def is_actice(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id) # python2
        except NameError:
            return str(self.id)     # python3
    @staticmethod 
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() is None:
            return True 
        else:
            return False
        # version = 2
    @staticmethod 
    def make_unique_emali(email):
        if User.query.filter_by(email=email).first() is None:
            return True 
        else:
            return False
        # while True:
            # new_nickname = nickname + str(version)
            # if User.query.filter_by(nickname=new_nickname).first() is None:
                # return new_nickname
            # version += 1

    def follow(self, user):
        if not self.is_following(user):
            self.followed_users.append(user)
            return self


    def unfollow(self, user):
        if self.is_following(user):
            self.followed_users.remove(user)
            return self

    def is_following(self, user):
        return self.followed_users.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Post.query.join(followers,(followers.c.followed_id==Post.user_id))\
                .filter(followers.c.fans_id==self.id)\
                .order_by(Post.timestamp.desc())

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Post(db.Model):
    __searchable__ = ['body']

    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))
    def __repr__(self):
        return '<Post %r>' % (self.body)

    # if sys.version_info < (3,0):
        # import flask_whooshalchemy
        # flask_whooshalchemy.whoosh_index(current_app._get_current_object(), Post)


class RequestInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(20))
    agent = db.Column(db.String(250))
    cookie = db.Column(db.String(700))

