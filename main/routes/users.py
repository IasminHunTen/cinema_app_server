from flask_restx import Resource
from sqlalchemy.exc import IntegrityError
import json

from ..extra_modules import api
from ..custom_exceptions import SQLDuplicateException
from ..controllers import User
from ..serializable import user_post_model, user_get_model
from ..utils import inject_validated_payload, doc_resp, crop_sql_err
from ..models import UserPost, GetUsers
from ..constants.req_responses import *
from ..constants import SQL_DUPLICATE_ERR


ns = api.namespace('users')


@ns.errorhandler(SQLDuplicateException)
def _(error):
    return {'message': str(error)}, 409


@ns.route('/')
@ns.response(*doc_resp(UPDATE_RESP))
class UserResource(Resource):

    @ns.response(*doc_resp(CREATE_RESP))
    @ns.expect(user_post_model)
    @inject_validated_payload(UserPost())
    def post(self, payload):
        try:
            User(payload['username'], payload['email'], payload['password']).db_store()
        except IntegrityError as ie:
            raise SQLDuplicateException(SQL_DUPLICATE_ERR.format(crop_sql_err(str(ie._sql_message))))
        return CREATE_RESP

    @ns.response(*doc_resp(FETCH_RESP))
    @ns.marshal_list_with(user_get_model)
    def get(self):
        return GetUsers().dumps(User.query.all()), 200



