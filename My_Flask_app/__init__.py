from flask import Flask 
from .models import db, UserData
from flask_mail import Mail, Message
from flask_login import LoginManager
import os


GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


app = Flask(__name__)
from My_Flask_app import forms, routes

db.init_app(app)
mail = Mail(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:shar@localhost/Information'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = '75e64d694b5c6602148044c51106738c'


app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "aydensharu@gmail.com"
app.config["MAIL_PASSWORD"] = "momdadbrosharook"
app.config["MAIL_DEFAULT_SENDER"] = "aydensharu@gmail.com"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail= Mail(app)


my_login_manager = LoginManager()
my_login_manager.init_app(app)
my_login_manager.login_view = ('login','create')


@app.before_first_request
def create_table():
    db.create_all()


@my_login_manager.user_loader
def load_user(id):
    return UserData.query.get(id)






