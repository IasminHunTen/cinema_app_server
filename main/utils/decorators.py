import jwt
from marshmallow import ValidationError
import json
from werkzeug.exceptions import BadRequest
from flask import request, current_app as app

from extra_modules import api, AuthException


def inject_validated_payload(schema):
    def decorator(f):
        def wrapper(*args, **kwargs):
            try:
                payload = schema.load(api.payload)
            except ValidationError as ve:
                raise BadRequest(json.dumps(ve.messages))
            return f(*args, **kwargs, payload=payload)
        return wrapper
    return decorator


def required_login(as_admin=False):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if 'token' not in request.args:
                raise AuthException('Auth Token is missing')
            try:
                token_data = jwt.decode(request.args.get('token'), app.config['SECRET_KEY'], 'HS256')
            except jwt.PyJWTError as e:
                raise AuthException(e)
            if as_admin and not token_data.get('isAdmin'):
                raise AuthException('Admin rights are needed')
            return f(*args, **kwargs, token_data=token_data)
        return wrapper
    return decorator






