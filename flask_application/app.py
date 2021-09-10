from enum import unique
import json
import os
from oauthlib.oauth2.rfc6749.endpoints import authorization
import requests


from flask import Flask , render_template, redirect, request, url_for, session,flash
from models import db, UserData
from flask_login import (
    LoginManager,
    current_user,
    login_manager,
    login_required,
    login_user,
    logout_user)

from oauthlib.oauth2 import WebApplicationClient
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
db.init_app(app)

GOOGLE_CLIENT_ID = "999814284602-q8ne5spkkbns82sae8rq6afunm4uji8i.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "5IMzjhN9E19z-lNd1YnSYqk5"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sharook@localhost/credentials'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.secret_key = "sha"

my_login_manager = LoginManager()
my_login_manager.init_app(app)
my_client = WebApplicationClient(GOOGLE_CLIENT_ID)


@my_login_manager.user_loader
def load_user(email):
    return UserData.query.filter_by(email =email)


@app.before_first_request
def create_table():
    db.create_all()


@app.route('/')
def index():
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email
            )
        )
    else:
        return '<a class="button" href="/googlelogin">Google Login</a>'

@app.route('/register', methods = ["POST","GET"])
def create():
    if request.method == "POST":
        id,username, email, password = request.form["id"], request.form["username"], request.form["email"], request.form["password"]
        if username.strip()=="":
            messsage = "username Not be empty"
            return render_template('register_form.html',msg=messsage)
        if email.strip() =="":
            email_error = "Email not be empty"
            return render_template('register_form.html',email_err=email_error)
        if password.strip() =="":
            password_error = "Password not be empty"
            return render_template('register_form.html',pw_err=password_error)

        else:
            user = UserData(id=id,username=username,email=email,password=password)
            db.session.add(user)
            db.session.commit()
            session["email"] = email
            session["password"] = password
            
            return redirect(url_for("user"))
    else:
        return render_template('register_form.html')


@app.route("/user")
def user():
    flash("user logined successfully")
    if  "email" and "password" in session:
        user_email = session["email"]
        user_password = session["password"]
        return render_template('user.html', em=user_email, pwd=user_password)
    else:
        redirect(url_for("register"))


@app.route('/login')
def login():
    return render_template('login_form.html')



def google_login_provider():
    return requests.get("https://accounts.google.com/.well-known/openid-configuration").json()



@app.route('/googlelogin')
def google_login():
    get_login_provider=google_login_provider()
    authorization_endpoint = get_login_provider["authorization_endpoint"]
    request_uri = my_client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri="http://127.0.0.1:5000"+"/blog",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route('/blog')
def callback():
    code = request.args.get("code")
    get_provider_cfg = google_login_provider()
    token_endpoint = get_provider_cfg["token_endpoint"]

    token_url, headers, body = my_client.prepare_token_request(
    token_endpoint,
    authorization_response=request.url,
    redirect_url=request.base_url,
    code=code
    )
    token_response = requests.post(
    token_url,
    headers=headers,
    data=body,
    auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    my_client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = get_provider_cfg["userinfo_endpoint"]
    uri, headers, body = my_client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        # unique_id = userinfo_response.json()["sub"]
        unique_id = "12345678"
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
        password = "sha"
    else:
        return "User email not available or not verified by Google.", 400


    user = UserData(id =unique_id, username=users_name, email=users_email, password=password)
    db.session.add(user)
    db.session.commit()

    if not UserData.query.get(unique_id):
        UserData.create(unique_id, users_name, users_email,password)
        db.session.add(user)
        db.session.commit()
    user.is_active = True
    login_user(user)
    return redirect(url_for("/"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("/"))




if __name__ == '__main__':
    app.run(debug=True)
