from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

auth_in_header = {
    'token': {
        'type': 'auth',
        'in': 'header',
        'name': 'Auth Token'
    }
}


class SQLDuplicateException(Exception):
    pass


class AuthException(Exception):
    pass


api = Api()
db = SQLAlchemy()
flask_marshal = Marshmallow()


@api.errorhandler(SQLDuplicateException)
def _sql_err(error):
    return {'SQLError': str(error)}, 409


@api.errorhandler(AuthException)
def _auth_err(error):
    return {'AuthError': str(error)}, 401


