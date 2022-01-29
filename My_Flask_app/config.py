from os import environ

SECRET_KEY = environ.get('SECRET_KEY')

# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:shar@localhost/Information'
SQLALCHEMY_DATABASE_URI = ' postgres://iuzbecbpybtrvg:70ecee323a993a2e4ef23c9d67e3a33c13170882f8af650327e67f1fd0cea9e8@ec2-107-21-146-133.compute-1.amazonaws.com:5432/dem7s52dbopn3f'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
FLASK_ADMIN_SWATCH = 'Cosmo'



   