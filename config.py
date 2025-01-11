import os

SECRET_KEY = "secret-key-sdsfs"
FLASK_DEBUG = 1
SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = os.path.join(os.getcwd(),'app','user', 'static', 'images')