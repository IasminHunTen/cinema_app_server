import os


class Config:
    SWAGGER_UI_JSONEDITOR = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    START_HOUR = os.getenv('START_HOUR')
    LIMIT_HOUR = os.getenv('LIMIT_HOUR')
    GAP_BETWEEN_MOVIES = os.getenv('GAP_BETWEEN_MOVIES')
    STANDARD_PRICE = os.getenv('STANDARD_PRICE')
    APP_NAME = os.getenv('APP_NAME')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL')
