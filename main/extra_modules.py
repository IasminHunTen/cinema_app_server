from flask_restx import Api, fields
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


class SQLDuplicateException(Exception):
    pass


class AuthException(Exception):
    pass


class NotFound(Exception):
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


@api.errorhandler(NotFound)
def _not_found_err(error):
    return {'Not Found': str(error)}, 404


class DictItem(fields.Raw):
    def output(self, key, obj, *args, **kwargs):
        try:
            dct = getattr(obj, self.attribute)
        except AttributeError:
            return {}
        return dct or {}



