
"""Class-based Flask app configuration."""
import os
from sqlalchemy import create_engine, exc,desc,or_,and_



class Config:
    SECRET_KEY ="geghuegtyuur56irfj8rrytrghgrrryytheugtr" # os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI ='mysql+pymysql://root:sword@localhost/imarket_deploy' #os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_RECYCLE = 229
    SQLALCHEMY_POOL_TIMEOUT =20

    conn = create_engine('mysql+pymysql://root:sword@localhost/imarket_deploy',pool_timeout=20, pool_recycle=229)#isoko!2020!*
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')


