from ..extra_modules import api
from flask_restx import fields

user_post_model = api.model('UserPostSchema', {
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

user_get_model = api.model('UsersGetSchema', {
    'id': fields.String(),
    'username': fields.String(),
    'email': fields.String(),
    'admin': fields.Boolean
})

user_token_model = api.model('UserTokenSchema', {
    'token': fields.String()
})


