import os
DEBUG       = True
SECRET_KEY  = os.urandom(24)

DIALECT     = 'mysql'
DRIVER      = 'pymysql'
USERNAME    = 'root'
PASSWORD    = '123'
HOST        = '127.0.0.1'
PORT        = '3306'
DARABSE     = 'db_demo5'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,
                                                                       DRIVER,USERNAME,PASSWORD,HOST,PORT,DARABSE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO=False
# 后台session_id键值
ADMIN_SESSION_ID = 'a6273a8b622104d4d63d0'

MAIL_SERVER         = 'smtp.163.com'
MAIL_USERNAME       = 'you1365831278@163.com'
MAIL_PASSWORD       = 'you134223'
MAIL_PORT           = '25'
MAIL_DEFAULT_SENDER = "you1365831278@163.com"


