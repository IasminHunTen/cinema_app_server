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
            if 'Token' not in request.headers:
                raise AuthException('Auth Token is missing')
            try:
                token_payload = jwt.decode(request.headers.get('Token'), app.config['SECRET_KEY'], 'HS256')
            except jwt.PyJWTError as e:
                raise AuthException(e)
            if as_admin and not token_payload.get('isAdmin'):
                raise AuthException('Admin rights are needed')
            return f(*args, **kwargs, token_payload=token_payload)
        return wrapper
    return decorator






