from flask import Flask 
from .models import db, UserData
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
admin = Admin(app,name="My-Admin", template_mode='bootstrap3')
from My_Flask_app import forms, routes

db.init_app(app)
with app.app_context():
    db.create_all()

app.config['FLASK_ADMIN_SWATCH'] = 'Cosmo'
app.config.from_pyfile('settings.py')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:shar@localhost/Information'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

my_login_manager = LoginManager()
my_login_manager.init_app(app)
my_login_manager.login_view = ('login','create')


@app.before_first_request
def create_table():
    db.create_all()


@my_login_manager.user_loader
def load_user(id):
    return UserData.query.get(id)






