from os import environ

SECRET_KEY = environ.get('SECRET_KEY')

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:shar@localhost/Information'
# SQLALCHEMY_DATABASE_URI = ' postgres://wizwvackguifwg:662e1eb83c54be438ed25af8074574099ba8718ff56f28368ec0888f018e33ea@ec2-18-213-179-70.compute-1.amazonaws.com:5432/d3mo6hccsm4tjs'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
FLASK_ADMIN_SWATCH = 'Cosmo'



   