import os


class Config(object):
    SWAGGER_UI_JSONEDITOR = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
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








