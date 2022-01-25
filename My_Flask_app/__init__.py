from flask import Flask 
from .models import db, UserData
from flask_login import LoginManager
app = Flask(__name__)
from My_Flask_app import forms, routes


db.init_app(app)
with app.app_context():
    db.create_all()

app.config.from_pyfile('config.py')

my_login_manager = LoginManager()
my_login_manager.init_app(app)
my_login_manager.login_view = 'login'
my_login_manager.login_message = "You should login first"



@app.before_first_request
def create_table():
    db.create_all()

# @app.before_first_request
# def creating_admin():
#     user_name = "sharook"
#     email = "sharook@recentech.com"
#     password = "sharook23031999"
#     updating_data = UserData(username=user_name,email=email)
#     updating_data.set_password(password)
#     db.session.add(updating_data)
#     db.session.commit()
#     app.logger.info("Admin created successfully")
    
@my_login_manager.user_loader
def load_user(user_id):
    return db.session.query(UserData).get(user_id)





