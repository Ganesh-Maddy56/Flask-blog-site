from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, BooleanField, TextField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_login import current_user
from .models import UserData


class Registration_Form(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')



class Login_Form(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class Jobs_Form(FlaskForm):
    companyname = StringField('companyname')
    joblink = StringField('joblink')
    jd = StringField('jd',validators=[Length(max=1000)])
    salary = StringField('salary')
    eligibility = StringField('eligibility')
    submit = SubmitField('upload')


class AccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    picture = FileField('update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = UserData.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username is taken, please user another username")
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = UserData.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email is taken, please user another email")
    

class Search(FlaskForm):
    searched = StringField('searched',validators=[DataRequired()])
    submit = SubmitField('Submit')