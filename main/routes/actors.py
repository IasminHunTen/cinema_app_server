from flask import request
from flask_restx import Resource

from constants import CREATE_RESP, UPDATE_RESP, FETCH_RESP, ids_in_query
from extra_modules import api, NotFound
from controllers import Actor
from serializable.actor import *
from utils import inject_validated_payload, doc_resp
from models.actor import *

ns = api.namespace('actors')


@ns.route('/')
class ActorsResource(Resource):
    @ns.response(*doc_resp(CREATE_RESP))
    @ns.expect(actor_post_model)
    @inject_validated_payload(PostActor())
    def post(self, payload):
        Actor(**payload).db_store()
        return CREATE_RESP

    @ns.response(*doc_resp(UPDATE_RESP))
    @ns.expect(actor_put_model)
    @inject_validated_payload(PutActor())
    def put(self, payload):
        try:
            Actor.edit_actor(**payload)
        except NotFound as nf:
            raise nf
        return UPDATE_RESP

    @ns.response(*doc_resp(UPDATE_RESP))
    @ns.expect(actor_delete_model)
    @inject_validated_payload(DeleteActor())
    def delete(self, payload):
        try:
            Actor.delete_actor(**payload)
        except NotFound as nf:
            raise nf
        return UPDATE_RESP

    @ns.response(*doc_resp(FETCH_RESP))
    @ns.marshal_list_with(actor_get_model)
    @ns.doc(params=ids_in_query)
    def get(self):
        schema = GetActor(many=True)
        ids = request.args.get('ids')
        if not ids:
            return schema.dump(Actor.fetch_actors()), 200
        return schema.dump(Actor.fetch_actors(ids.split())), 200











