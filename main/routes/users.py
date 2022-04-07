from flask_restx import Resource
from flask import current_app as app, request
from sqlalchemy.exc import IntegrityError
import jwt
from datetime import datetime, timedelta
from werkzeug.exceptions import BadRequest

from extra_modules import api, SQLDuplicateException
from controllers import User, UserDevices, UserFavoriteGenres
from serializable import user_post_model, user_token_model, get_user_devices_model, ufg_model
from utils import inject_validated_payload, doc_resp, crop_sql_err, required_login, debug_print
from models import UserPost, GetUsers, GetUserDeviceSchema, UFGSchema
from constants.req_responses import *
from constants import SQL_DUPLICATE_ERR, auth_in_header, string_from_query

ns = api.namespace('users')


def generate_token(user):
    token = jwt.encode({
        'id': user.id,
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


@ns.route('/auth')
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


@ns.route('/user-devices')
class UserDeviceResource(Resource):
    @ns.response(*doc_resp(FETCH_RESP))
    @ns.response(*doc_resp(NOT_FOUND))
    @ns.marshal_list_with(get_user_devices_model)
    @ns.doc(params=auth_in_header)
    @required_login()
    def get(self, token_data):
        user_devices = UserDevices.fetch_user_device(token_data.get('id'))
        if not user_devices:
            raise NOT_FOUND('User not found')
        return GetUserDeviceSchema(many=True).dump(user_devices), 200

    @ns.response(*doc_resp(DELETE_RESP))
    @ns.doc(params=auth_in_header)
    @ns.doc(params=string_from_query('device_serial_number'))
    @required_login()
    def delete(self, token_data):
        dsn = request.args.get('device_serial_number')
        if dsn is None:
            raise BadRequest('Missing device serial number from query')
        UserDevices.delete(token_data['id'], dsn.split())
        return DELETE_RESP


@ns.route('/user_favorite_genres')
@ns.response(*doc_resp(UNAUTHORIZED))
class UFGResource(Resource):
    @ns.response(*doc_resp(CREATE_RESP))
    @ns.response(*doc_resp(BAD_REQUEST))
    @ns.doc(params=string_from_query('genre_ids'))
    @ns.doc(params=auth_in_header)
    @required_login()
    def post(self, token_data):
        genres_ids = request.args.get('genre_ids')
        if genres_ids is None:
            raise BadRequest('At Least One genres need to be chosen')
        for genre_id in genres_ids.split():
            UserFavoriteGenres(token_data.get('id'), genre_id).db_store()
        return CREATE_RESP

    @ns.response(*doc_resp(UPDATE_RESP))
    @ns.doc(params=string_from_query('genre_ids'))
    @ns.doc(params=auth_in_header)
    @required_login()
    def put(self, token_data):
        genres_ids = request.args.get('genre_ids')
        updated_genres_ids = {} if genres_ids is None else set(genres_ids.split())
        UserFavoriteGenres.edit_favorite_genre(token_data.get('id'), updated_genres_ids)
        return UPDATE_RESP

    @ns.response(*doc_resp(FETCH_RESP))
    @ns.doc(params=auth_in_header)
    @ns.marshal_with(ufg_model)
    @required_login()
    def get(self, token_data):
        return UFGSchema().dump(UserFavoriteGenres.favorite_genres_for_user(token_data.get('id'))), 200









