import os


class Config:
    SWAGGER_UI_JSONEDITOR = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    START_HOUR = int(os.getenv('START_HOUR'))
    LIMIT_HOUR = int(os.getenv('LIMIT_HOUR'))
    GAP_BETWEEN_MOVIES = int(os.getenv('GAP_BETWEEN_MOVIES'))
    STANDARD_PRICE = float(os.getenv('STANDARD_PRICE'))
    APP_NAME = os.getenv('APP_NAME')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
