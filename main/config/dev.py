import os


class Config(object):
    SWAGGER_UI_JSONEDITOR = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    TOKEN_VALIDITY = 7200
    START_HOUR = 12
    LIMIT_HOUR = 23
    GAP_BETWEEN_MOVIES = 30
    STANDARD_PRICE = 20
    APP_NAME = 'Hunty Cinema'
    MAIL_SERVER = 'outlook.office365.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'huntycinema@outlook.com'
    MAIL_PASSWORD = 'berlinDefence'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False








