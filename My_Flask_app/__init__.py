from flask import Flask 
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app,session_options={"autoflush": False})


from My_Flask_app import forms, routes
from My_Flask_app.models import UserData

app.config.from_pyfile('config.py')
migrate = Migrate(app,db)


my_login_manager = LoginManager()
my_login_manager.init_app(app)
my_login_manager.login_view = 'login'
my_login_manager.login_message = "You should login first"


@my_login_manager.user_loader
def load_user(user_id):
    return db.session.query(UserData).get(user_id)



if __name__ == '__main__':
    app.debug = True
    app.run()