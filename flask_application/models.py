from re import T
from flask.scaffold import F
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.sql.sqltypes import VARCHAR, BigInteger

db = SQLAlchemy(session_options={"autoflush": False})

class UserData(db.Model):
    __tablename__ = "users_detail"

    id = db.Column(db.BIGINT,primary_key=True)
    username = db.Column(db.String(100),unique=True,nullable=False)
    email = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(100),nullable=False)

    def __init__(self, id,username,email,password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
 
    def __repr__(self):
        return  f"{self.id}:{self.email}"
