from flask import render_template, redirect, request, url_for, flash, session, abort
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user)
import flask_login
from My_Flask_app.forms import AccountForm, Registration_Form,Login_Form, Jobs_Form
from My_Flask_app.models import db,UserData,JobsFromDataBase
from My_Flask_app import app
import os
import secrets
from PIL import Image
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


admin = Admin(app,name="My-Admin", template_mode='bootstrap4')
@app.errorhandler(404)
def errorpage(e):
    return render_template('Error_page.html'),404

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
            print(user.get_id())
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
@login_required
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
@login_required
def logout():
    print(current_user.id)
    logout_user()
    flash('Loged-Out Successfull')
    return redirect(url_for('login'))


@app.route('/ConsistentJobUpdates')
def jobs():
    page = request.args.get('page',1,type=int)
    data = JobsFromDataBase.query.paginate(page=page,per_page=7)
    return render_template("job_template.html",data = data)

class Adminaccessecure(ModelView):

    def is_accessible(self):
        return flask_login.current_user.is_authenticated and current_user.id == 1
           
admin.add_view(Adminaccessecure(JobsFromDataBase,db.session))
admin.add_view(Adminaccessecure(UserData,db.session))


@app.route('/contact',methods=["POST","GET"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        print(name, email, message) 
        flash("Thanks For Reaching Us")
        return redirect(url_for('contact'))
    else:
        return render_template('contact_form.html')

    
