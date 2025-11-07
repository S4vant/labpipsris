import os
from . import creds
NAME, USER, PASSWORD, PORT, HOST, SECRET_KEY = creds.creds()
# print(NAME, USER, PASSWORD, PORT, HOST, SECRET_KEY)

class Config:
    SECRET_KEY = SECRET_KEY
    
    # MySQL configuration
    MYSQL_HOST = HOST
    MYSQL_USER = USER
    MYSQL_PASSWORD = PASSWORD
    MYSQL_DB = NAME
    MYSQL_PORT = PORT
    
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True
    }