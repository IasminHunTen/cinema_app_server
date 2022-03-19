from flask_restx import Resource
from flask import current_app as app
from sqlalchemy.exc import IntegrityError
import jwt
from datetime import datetime, timedelta

from extra_modules import api, SQLDuplicateException
from controllers import User
from serializable import user_post_model, user_token_model
from utils import inject_validated_payload, doc_resp, crop_sql_err, required_login
from models import UserPost, GetUsers
from constants.req_responses import *
from constants import SQL_DUPLICATE_ERR, auth_in_header

ns = api.namespace('users')


def generate_token(user):
    token = jwt.encode({
        'username': user.username,
        'email': user.email,
        'isAdmin': user.isAdmin,
        'exp': datetime.now() + timedelta(hours=2)
    }, key=app.config['SECRET_KEY'])

    return {'token': token}


@ns.route('/')
class UserResource(Resource):
    @ns.doc(params=auth_in_header)
    @ns.response(*doc_resp(FETCH_RESP))
    @required_login(as_admin=True)
    def get(self, token_data):
        user_list = User.query.all()
        return GetUsers(many=True).dump(user_list), 200


@ns.route('/auth/')
class RegisterResource(Resource):
    @ns.response(*doc_resp(CREATE_RESP))
    @ns.expect(user_post_model)
    @ns.marshal_with(user_token_model)
    @inject_validated_payload(UserPost())
    def post(self, payload):
        try:
            user = User(payload['username'], payload['email'], payload['password'])
            user.db_store()
        except IntegrityError as ie:
            raise SQLDuplicateException(SQL_DUPLICATE_ERR.format(crop_sql_err(str(ie._sql_message))))
        return generate_token(user)



