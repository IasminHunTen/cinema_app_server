from marshmallow import ValidationError
import json
from ..extra_modules import api
from werkzeug.exceptions import BadRequest


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




