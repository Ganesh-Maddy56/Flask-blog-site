from os import environ

SECRET_KEY = environ.get('SECRET_KEY')

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:shar@localhost/Information'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
FLASK_ADMIN_SWATCH = 'Cosmo'



   