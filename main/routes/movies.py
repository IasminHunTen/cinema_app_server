from flask_restx import Resource

from constants import auth_in_header
from constants.req_responses import *
from extra_modules import SQLDuplicateException
from utils import doc_resp, inject_validated_payload, required_login, MovieRapidAPI
from models.movie import *
from serializable.movie import *
from controllers import Movie

ns = api.namespace('movies')

@ns.route('/')
@ns.response(BAD_REQUEST)
class MovieResource(Resource):

    mra_client = MovieRapidAPI()

    @ns.response(*doc_resp(CREATE_RESP))
    @ns.response(*doc_resp(UNAUTHORIZED))
    @ns.response(*doc_resp(DUPLICATED))
    @ns.expect(post_movie_model)
    @ns.doc(params=auth_in_header)
    @required_login(as_admin=True)
    @inject_validated_payload(PostSchema())
    def post(self, payload):
        try:
            movie_attributes = self.mra_client.movie_factory(**payload)
            Movie(**movie_attributes).db_store()
        except SQLDuplicateException as sqe:
            raise sqe
        return CREATE_RESP

    @ns.response(*doc_resp(FETCH_RESP))
    @ns.marshal_list_with(get_movie_model)
    def get(self):
        return GetSchema(many=True).dump(Movie.fetch_movies())

    @ns.response(*doc_resp(UPDATE_RESP))
    @ns.expect(put_movie_model)
    @inject_validated_payload(PutSchema())
    def put(self, payload):
        Movie.edit_movie(**payload)
        return UPDATE_RESP

    @ns.response(*doc_resp(DELETE_RESP))
    @ns.expect(delete_movie_model)
    @inject_validated_payload(DeleteSchema())
    @ns.doc(params=auth_in_header)
    @required_login(as_admin=True)
    def delete(self, payload):
        Movie.delete_movies(**payload)
        return DELETE_RESP



