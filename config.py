import os
# from models import base_dir

# 資料夾的絕對位置
base_dir = os.path.dirname(os.path.abspath(__name__))

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dowepfjp0wk1'
    SECURITY_PASSWORD_SALT = 'jidopajdh'
    SECURITY_PASSWORD_HASH = 'bcrypt'