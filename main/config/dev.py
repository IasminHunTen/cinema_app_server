class Config(object):
    SWAGGER_UI_JSONEDITOR = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dont tell anyone'
    START_HOUR = 12
    LIMIT_HOUR = 23
    GAP_BETWEEN_MOVIES = 30
    STANDARD_PRICE = 20







