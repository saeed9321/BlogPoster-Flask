from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[length(min=4, max=20)])
    password = PasswordField('Password', validators=[length(min=5)])
    submit = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[length(min=4, max=20)])
    password = PasswordField('Password', validators=[length(min=5)])
    confirm_password = PasswordField('Confirm password', validators=[EqualTo('password')])
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Register')

# not used yet
class UpdateForm(FlaskForm):
    username = StringField('Username', validators=[length(min=4, max=20)])
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Update')

class BlogForm(FlaskForm):
    submit = SubmitField('Post a blog')

class UploadImage(FlaskForm):
    submit = SubmitField('Submit')
