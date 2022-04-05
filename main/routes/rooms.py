from flask_restx import Resource

from constants import auth_in_header, CREATE_RESP, UPDATE_RESP, FETCH_RESP, DELETE_RESP, UNAUTHORIZED
from utils import doc_resp, inject_validated_payload, required_login
from models.room import *
from serializable.room import *
from controllers import Room
from extra_modules import api

ns = api.namespace('rooms')


@ns.route('/')
@ns.response(*doc_resp(UNAUTHORIZED))
class RoomResource(Resource):

    @ns.response(*doc_resp(FETCH_RESP))
    @ns.marshal_list_with(get_room_model)
    @ns.doc(params=auth_in_header)
    @required_login(as_admin=True)
    def get(self, token_data):
        return GetRoom(many=True).dump(Room.fetch_all())

    @ns.response(*doc_resp(CREATE_RESP))
    @ns.expect(post_room_model)
    @inject_validated_payload(PostRoom())
    @ns.doc(params=auth_in_header)
    @required_login(as_admin=True)
    def post(self, payload, token_data):
        Room(**payload).db_store()
        return CREATE_RESP

    @ns.response(*doc_resp(UPDATE_RESP))
    @ns.expect(put_room_model)
    @inject_validated_payload(PutRoom())
    @ns.doc(params=auth_in_header)
    @required_login(as_admin=True)
    def put(self, payload, token_data):
        try:
            Room.alter_room(**payload)
            return UPDATE_RESP
        except Exception as e:
            raise e

    @ns.response(*doc_resp(DELETE_RESP))
    @ns.expect(delete_room_model, validate=False)
    @inject_validated_payload(DeleteRoom())
    @ns.doc(params=auth_in_header)
    @required_login(as_admin=True)
    def delete(self, payload, token_data):
        try:
            Room.delete_room(**payload)
            return DELETE_RESP
        except Exception as e:
            raise e



