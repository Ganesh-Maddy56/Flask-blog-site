from wtforms.validators import URL
from My_Flask_app import app , GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from flask import render_template, redirect, request, url_for, flash
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user)
from My_Flask_app.forms import AccountForm, Registration_Form,Login_Form
from My_Flask_app.models import db,UserData
from oauthlib.oauth2 import WebApplicationClient

import json
import os
import requests
import smtplib
import secrets
from PIL import Image



@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("newindex.html")
    else:
        return render_template("newindex.html")


@app.route('/register',methods=["POST","GET"])
def create():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == "POST":
        form = Registration_Form()
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            if UserData.query.filter_by(email=email).first():
                flash("Email already registered")
                return render_template("register_form.html",form = form)
            
            user = UserData(username=username, email= email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Account created successfully !")

            # message = "you registered for my app"
            # server = smtplib.SMTP("smtp.gmail.com",587)
            # server.starttls()
            # server.login("aydensharu@gmail.com", "momdadbrosharook")
            # server.sendmail("aydensharu@gmail.com", email, message )
            return redirect(url_for('login'))
        else:
            return render_template("register_form.html",form=form)

    else:
        form = Registration_Form()      
        return render_template("register_form.html",form=form)



@app.route('/login',methods=["POST","GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == "POST":
        form = Login_Form()
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = UserData.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("You Have to register for login, or your password may be invalid")
                return render_template('login_form.html',form=form)
        else:
            return render_template("login_form.html",form=form)

    else:
        form = Login_Form()
        return render_template("login_form.html",form=form)

my_client = WebApplicationClient(GOOGLE_CLIENT_ID)

def google_login_provider():
    return requests.get("https://accounts.google.com/.well-known/openid-configuration").json()

@app.route('/googlelogin')
def google_login():
    get_login_provider=google_login_provider()
    authorization_endpoint = get_login_provider["authorization_endpoint"]
    request_uri = my_client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri="http://127.0.0.1:5000"+"/new",
        scope=["email", "profile"],
    )
    return redirect(request_uri)


@app.route('/new')
def callback():
    code = request.args.get("code")
    get_login_cfg = google_login_provider()
    token_endpoint = get_login_cfg["token_endpoint"]

    token_url, headers, body = my_client.prepare_token_request(
    token_endpoint,
    authorization_response=request.url,
    redirect_url="http://127.0.0.1:5000/new",
    code=code
    )
    token_response = requests.post(
    token_url,
    headers=headers,
    data=body,
    auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    my_client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = get_login_cfg["userinfo_endpoint"]
    uri, headers, body = my_client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)


    if userinfo_response.json().get("email_verified"):
        # unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    user = UserData.query.filter_by(email=users_email).first()
    if user:
        login_user(user)
        return redirect(url_for("index"))
    
    else:
        user = UserData(username=users_name, email=users_email)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("index"))


@app.route("/account",methods=["POST","GET"])
def account():
    if current_user.is_authenticated:
        form = AccountForm()
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_user_pic(form.picture.data)
                current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            return redirect(url_for('account'))

        elif request.method == "GET":
            form.username.data = current_user.username
            form.email.data = current_user.email

        image_file = url_for('static',filename='profile_pics/' + current_user.image_file)
        return render_template('account.html',image_file=image_file,form=form)

    else:
        flash("You Have to login first")
        return redirect(url_for('login'))

 
def save_user_pic(User_picture):
    secret = secrets.token_hex(8)
    _, f_ext = os.path.splitext(User_picture.filename)
    picture_name = secret + f_ext
    file_path = os.path.join(app.root_path, 'static/profile_pics', picture_name)
    img_size = (125,125)
    i = Image.open(User_picture)
    i.thumbnail(img_size)
    i.save(file_path)
    return picture_name


@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("Loged out successfull !")
        return redirect(url_for('index'))
    else:
        flash("No User loged In")
        return redirect(url_for('login')) 