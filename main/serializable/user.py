from ..extra_modules import api
from flask_restx import fields


user_get_model = api.model('UsersGetSchema', {
    'id': fields.String(),
    'username': fields.String(),
    'email': fields.String()
})


