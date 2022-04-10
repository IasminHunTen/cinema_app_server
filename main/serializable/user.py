from extra_modules import api
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

delete_user_model = api.model('DeleteUser', {
    'id': fields.String(required=True)
})

user_login_model = api.model('UserLoginSchema', {
    'username': fields.String(),
    'password': fields.String()
})

user_token_model = api.model('UserTokenSchema', {
    'token': fields.String()
})

user_prejudice_model = api.model('GetUserPrejudice', {
    'prejudice': fields.Float()
})

reset_password_model = api.model('ResetPassword', {
    'email': fields.String(required=True),
    'new_password': fields.String(required=True),
    'validation_code': fields.String(required=True)
})

voted_movie_model = api.model('VotedMovieSchema', {
    'movies_id': fields.List(fields.String())
})



