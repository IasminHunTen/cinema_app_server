from flask import request
from flask_restx import Resource

from constants.req_responses import *
from constants import ids_in_query
from extra_modules import NotFound
from utils import doc_resp, inject_validated_payload
from models.genre import *
from serializable.genre import *
from controllers import Genre

ns = api.namespace('genres')


@ns.route('/')
@ns.response(*doc_resp(UNAUTHORIZED))
class GenresResource(Resource):

    @ns.response(*doc_resp(FETCH_RESP))
    @ns.response(*doc_resp(NOT_FOUND))
    @ns.doc(params=ids_in_query)
    @ns.marshal_list_with(genre_get_model)
    def get(self):
        schema = GetGenres(many=True)
        ids = request.args.get('ids')
        try:
            if ids is None:
                return schema.dump(Genre.fetch()), 200
            return schema.dump(Genre.fetch(ids.split())), 200
        except NotFound as nf:
            raise nf

    @ns.response(*doc_resp(CREATE_RESP))
    @ns.expect(genre_post_model)
    @inject_validated_payload(PostGenre())
    def post(self, payload):
        Genre(**payload).db_store()
        return CREATE_RESP

    @ns.response(*doc_resp(UPDATE_RESP))
    @ns.response(*doc_resp(NOT_FOUND))
    @ns.response(*doc_resp(DUPLICATED))
    @ns.expect(genre_put_model)
    @inject_validated_payload(PutGenre())
    def put(self, payload):
        try:
            Genre.db_alter(**payload)
            return UPDATE_RESP
        except Exception as e:
            raise e

    @ns.response(*doc_resp(DELETE_RESP))
    @ns.response(*doc_resp(NOT_FOUND))
    @ns.expect(genre_delete_model)
    @inject_validated_payload(DeleteGenre())
    def delete(self, payload):
        try:
            Genre.db_delete(**payload)
            return DELETE_RESP
        except NotFound as nf:
            raise nf
