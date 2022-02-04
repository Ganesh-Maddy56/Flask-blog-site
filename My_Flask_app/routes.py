from flask import render_template, redirect, request, url_for, flash, session, abort
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user)
import flask_login
from My_Flask_app.forms import AccountForm, Registration_Form,Login_Form,Search
from My_Flask_app.models import db,UserData,JobsFromDataBase,Blog,ProblemSolving
from My_Flask_app import app
import os
import secrets
from PIL import Image
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import smtplib

admin = Admin(app,name="Admin-Dashboard", template_mode='bootstrap4')
@app.errorhandler(404)
def errorpage(e):
    error_code = 404
    error = "Page you requested is not found :( ...."
    message = "Please check your typo"
    return render_template('Error_page.html',error=error_code,errormsg=error,msg=message,),404

@app.errorhandler(500)
def internal_error(e):
    error_code = 500
    error = "Internal server error, will update as soon as possible :( ...."
    message = "Error in our Server"
    return render_template('Error_page.html',error=error_code,errormsg=error,msg=message,),500

@app.route("/")
def index():
    code = ProblemSolving.query.all()
    data = code[-1]
    if current_user.is_authenticated:
        return render_template("landing_page.html",data=data)
    else:
        return render_template("landing_page.html",data=data)

@app.route('/ST-register',methods=["POST","GET"])
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


@app.route('/ST-login',methods=["POST","GET"])
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


@app.route("/ST-account",methods=["POST","GET"])
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

@app.route("/ST-logout")
@login_required
def logout():
    print(current_user.id)
    logout_user()
    flash('Loged-Out Successfull')
    return redirect(url_for('login'))

@app.route('/ST-ConsistentJobUpdates')
def jobs():
    page = request.args.get('page',1,type=int)
    data = JobsFromDataBase.query.paginate(page=page,per_page=12)
    return render_template("job_template.html",data = data)

class Adminaccessecure(ModelView):
    def is_accessible(self):
        return flask_login.current_user.is_authenticated and current_user.id==1 and current_user.email == "sharook@shastechy.com"
    
admin.add_view(Adminaccessecure(JobsFromDataBase,db.session,name='JOBS'))
admin.add_view(Adminaccessecure(UserData,db.session,name='USERS'))
admin.add_view(Adminaccessecure(Blog,db.session,name='BLOGS'))
admin.add_view(Adminaccessecure(ProblemSolving,db.session,name='Coding_Problems'))


@app.route('/ST-contact',methods=["POST","GET"])
def contact():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # server = smtplib.SMTP("smtp.gmail.com",587)
        # server.starttls()
        # server.login("mohmdsharook@gmail.com",environ.get('email'))
        # server.sendmail(from_addr="mohmdsharook@gmail.com",to_addrs=["mohmdsharook@gmail.com"],msg="Message from my website user -> {}\nUser E-mail address -> {}\n Message-> {}".format(name,email,message))
        flash("Thanks For Reaching Us")
        return redirect(url_for('contact'))
    else:
        return render_template('contact_form.html')

@app.route('/ST-ApplyJobFor/<string:comp_name>/<int:id>')
def joblink(comp_name,id):
    info = JobsFromDataBase.query.get(id)
    try:
        if info.id is not None:
            return render_template('JobDescription.html',info=info)
    except Exception:
        error_code = 404
        error = "Page you requested is not found :( ...."
        message = "Please check your typo"
        return render_template('Error_page.html',error=error_code,errormsg=error,msg=message,),404

@app.route('/ST-delete-user')
def delete_user():
    user_Data = UserData.query.get(current_user.id)
    try:
        if user_Data is not None:
            db.session.delete(user_Data)
            db.session.commit()
            flash("User deleted successfully !")
            return redirect(url_for('index'))
    except:
        flash("User not found!")
        return redirect(url_for('index'))

@app.route('/ST-blogs')
@app.route('/ST-blogs/<string:topic>/<int:id>')
def blogs(topic=None,id=None):
    form = Search()
    data = Blog.query.all()
    last_update = data[-1]
    if url_for(request.endpoint, **request.view_args) == '/ST-blogs':
        return render_template('blogs.html',form=form,datas = last_update,all_blog_topic=data)
    elif (topic != None and id!= None):
        query_blog = Blog.query.get(id)
        if query_blog is not None and query_blog.topic == topic:
            return render_template('blogs.html',form=form,clicked_id=query_blog,datas=last_update,all_blog_topic=data)
        else:
            error_code = 404
            error = "Page you requested is not found :( ...."
            message = "Please check your typo"
            return render_template('Error_page.html',error=error_code,errormsg=error,msg=message,),404
    else:
            error_code = 404
            error = "Page you requested is not found :( ...."
            message = "Please check your typo"
            return render_template('Error_page.html',error=error_code,errormsg=error,msg=message,),404

@app.route('/ST-SearchedResult', methods=["POST"])
def search():
    form = Search()
    blog = Blog.query
    if form.validate_on_submit():
        searched_for = form.searched.data
        blog = blog.filter(Blog.topic.like('%' + searched_for + '%'))
        blog = blog.order_by(Blog.id).all()
        no_of_data = len(blog)
        return render_template('SearchedContent.html',data=blog,searched=searched_for,no_of_data=no_of_data)
    return redirect(url_for('blogs'))

@app.route('/ST-ShowingBlog/<topic>/<int:id>')
def PerticularBLog(topic,id):
    blog = Blog.query.get(id)
    try:
        if blog.id is not None:
            return render_template('blogs.html',info=blog)
    except Exception:
        error_code = 404
        error = "Page you requested is not found :( ...."
        message = "Please check your typo"
        return render_template('Error_page.html',error=error_code,errormsg=error,msg=message,),404
