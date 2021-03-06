from flask_login.mixins import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from My_Flask_app import db

class UserData(db.Model,UserMixin):
   
    __tablename__ = "user"

    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    username = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(200),nullable=False,unique=True)
    password = db.Column(db.String(200))
    image_file = db.Column(db.String(20),nullable = True, default = "default.gif")
    registered_on  = db.Column(db.DateTime(),nullable=False,default= datetime.now().date())

    def set_password(self,password):
        self.password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)
 
    def __repr__(self):
        return  f"{self.id}:{self.email}:{self.username}"
  
    def is_active(self):
        return True
    
    def is_authenticated(self):
        return True
    
    def get_id(self):
        return self.id

class JobsFromDataBase(db.Model,UserMixin):
    cur_date = datetime.now()
    date = cur_date.date()

    __tablename__ = "jobs"
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    companyname = db.Column(db.String(100),nullable=False)
    jd = db.Column(db.String(300),nullable=False)
    salary = db.Column(db.String(100), nullable=False)
    eligibility = db.Column(db.String(100),nullable=False)
    branch = db.Column(db.String(100),nullable=False)
    created_date = db.Column(db.DateTime(),default = date)
    skills_required = db.Column(db.String(2000))
    responsiblities = db.Column(db.String(2000))
    official_link = db.Column(db.String(200),nullable=False)
    location = db.Column(db.String(100))
    end_date = db.Column(db.DateTime(),nullable=True)

    def __repr__(self):
        return  f"{self.id}:{self.companyname}:{self.jd}:{self.eligibility}"


class Blog(db.Model,UserMixin):
    __tablename__ = 'dailyblogs'
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    topic = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text(),nullable=False)
    posted_date = db.Column(db.DateTime(),default=datetime.now().date())

    def __repr__(self) -> str:
        return f"{self.id}:{self.content}:{self.posted_date}"

class ProblemSolving(db.Model,UserMixin):
    __tablename__ = 'Problemsolving'
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    ques_topic = db.Column(db.String(100),nullable=False)
    question = db.Column(db.Text(),nullable=False)
    input = db.Column(db.Text(),nullable=False)
    output = db.Column(db.Text(),nullable=False)
    explanation = db.Column(db.Text(),nullable=False)
    code = db.Column(db.Text(),nullable=False)
    posted_date = db.Column(db.DateTime(),default=datetime.now().date())

    def __repr__(self) -> str:
        return f"{self.id}:{self.code}:{self.posted_date}"