from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = "anything"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['upload'] = 'project'
db = SQLAlchemy(app)
LoginManager = LoginManager(app)
LoginManager.login_view = 'login'
LoginManager.login_message_category = 'info'

from project import routes
