from datetime import date
from My_Flask_app import app,admin,ModelView
from flask import render_template, redirect, request, url_for, flash, session, abort
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user)
from My_Flask_app.forms import AccountForm, Registration_Form,Login_Form, Jobs_Form
from My_Flask_app.models import db,UserData,JobsFromDataBase

import os
import secrets
from PIL import Image


@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("HomePageBase.html")
    else:
        return render_template("HomePageBase.html")


@app.route('/register',methods=["POST","GET"])
def create():
    if current_user.is_authenticated:
        flash("Already LogedIn !")
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
            return redirect(url_for('login'))
        else:
            return render_template("register_form.html",form=form)

    else:
        form = Registration_Form()      
        return render_template("register_form.html",form=form)



@app.route('/login',methods=["POST","GET"])
def login():
    if current_user.is_authenticated:
        flash("Already logedIn !")
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
                flash("You Have to SignIn for login, or your password may be invalid")
                return render_template('login_form.html',form=form)
        else:
            return render_template("login_form.html",form=form)

    else:
        form = Login_Form()
        return render_template("login_form.html",form=form)


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
        render_template('HomePageBase.html',image_file = image_file)
        return render_template('account.html',image_file=image_file,form=form)

    else:
        flash("You Have to login first")
        return redirect(url_for('login'))
 
def save_user_pic(User_picture):
    secret = secrets.token_hex(8)
    _, f_ext = os.path.splitext(User_picture.filename) 
    picture_name = secret + f_ext
    file_path = os.path.join(app.root_path, 'static/profile_pics', picture_name)
    img_size = (120,120)
    i = Image.open(User_picture)
    i.thumbnail(img_size)
    i.save(file_path)
    return picture_name


@app.route("/logout")
def logout():
    if not current_user.is_authenticated:
        flash('No-User Loged-In, Login First')
        return redirect(url_for('login'))
    else:
        form = Login_Form()
        logout_user()
        flash('Loged-Out Successfull')
        return redirect(url_for('login'))


@app.route('/ConsistentJobUpdates')
def jobs():
    start = date(year=2022,month=1,day=1)
    end = date(year=2022, month=1, day=30)
    data = JobsFromDataBase.query.all()
    return render_template("job_template.html",data = data)

class AdminPageSecure(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return True
        else:
            abort(403)

admin.add_view(AdminPageSecure(JobsFromDataBase,db.session))
admin.add_view(AdminPageSecure(UserData,db.session))
