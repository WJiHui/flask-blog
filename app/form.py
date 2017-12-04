# encoding:utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email
from app.models import User

class LoginForm(FlaskForm):
    user = StringField('user', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class EditForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
    
    def __init__(self, original_nickname, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user is None:
            return True
        self.nickname.errors.append('This nickname is already use')
        return False


class RegisterForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

class PostForm(FlaskForm):
    post = TextAreaField('post', validators=[DataRequired()])


class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])

