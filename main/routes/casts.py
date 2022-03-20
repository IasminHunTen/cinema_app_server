from flask import request
from flask_restx import Resource

from constants import ids_in_query, auth_in_header
from constants.req_responses import *
from extra_modules import api, NotFound
from controllers import Cast
from serializable.cast import *
from utils import inject_validated_payload, doc_resp, required_login
from models.cast import *

ns = api.namespace('casts')


@ns.route('/')
@ns.response(*doc_resp(UPDATE_RESP))
class CastsResource(Resource):
    @ns.response(*doc_resp(CREATE_RESP))
    @ns.expect(cast_post_model)
    @ns.doc(params=auth_in_header)
    @required_login(as_admin=True)
    @inject_validated_payload(PostCast())
    def post(self, payload, token_data):
        Actor(**payload).db_store()
        return CREATE_RESP

    @ns.response(*doc_resp(UPDATE_RESP))
    @ns.expect(cast_put_model)
    @ns.doc(params=auth_in_header)
    @inject_validated_payload(PutCast())
    @required_login(as_admin=True)
    def put(self, payload, token_data):
        try:
            Cast.edit_actor(**payload)
        except NotFound as nf:
            raise nf
        return UPDATE_RESP

    @ns.response(*doc_resp(DELETE_RESP))
    @ns.expect(cast_delete_model)
    @ns.doc(params=auth_in_header)
    @inject_validated_payload(DeleteActor())
    @required_login(as_admin=True)
    def delete(self, payload, token_data):
        try:
            Cast.delete_actor(**payload)
        except NotFound as nf:
            raise nf
        return DELETE_RESP

    @ns.response(*doc_resp(FETCH_RESP))
    @ns.marshal_list_with(cast_get_model)
    @ns.doc(params=ids_in_query)
    def get(self):
        schema = GetCast(many=True)
        ids = request.args.get('ids')
        if not ids:
            return schema.dump(Cast.fetch_actors()), 200
        return schema.dump(Cast.fetch_actors(ids.split())), 200











