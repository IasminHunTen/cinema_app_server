import os


class Config(object):
    SWAGGER_UI_JSONEDITOR = True
    SQLALCHEMY_DATABASE_URI = 'postgres://ilcgdpualpwxot:fee320abb5bcd3cef686b58540f8ccceeb0a731e09b9e71fa4d723636240010b@ec2-54-80-123-146.compute-1.amazonaws.com:5432/ddd9i45em5tn84'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    START_HOUR = 12
    LIMIT_HOUR = 23
    GAP_BETWEEN_MOVIES = 30
    STANDARD_PRICE = 20
    APP_NAME = 'Hunty Cinema'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'cinema.mobile.app@gmail.com'
    MAIL_PASSWORD = 'BerlinDefence'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True








