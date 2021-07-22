
"""Class-based Flask app configuration."""
import os
from sqlalchemy import create_engine, exc,desc,or_,and_



class Config:
    SECRET_KEY ="geghuegtyuur56irfj8rrytrghgrrryytheugtr" # os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI ='mysql+pymysql://root:sword@localhost/MyBlock' #os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_RECYCLE = 229
    SQLALCHEMY_POOL_TIMEOUT =20
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
 

    MAX_CONTENT_LENGTH = 100 * 1024 * 1024    
    conn = create_engine('mysql+pymysql://root:sword@localhost/MyBlock',pool_timeout=20, pool_recycle=229)#isoko!2020!*
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "heretolearn1@gmail.com"
    MAIL_PASSWORD = "TeamPESA" #os.environ.get('EMAIL_PASS')
    DATA_UPLOAD_MAX_MEMORY_SIZE = 150242880 
