from flask_restx import Resource

from constants import auth_in_header
from constants.req_responses import *
from extra_modules import SQLDuplicateException
from utils import doc_resp, inject_validated_payload, required_login, MovieRapidAPI
from models.movie import *
from serializable.movie import *
from controllers import Movie, Cast, Genre, MovieGenres, MovieCast


ns = api.namespace('movies')


@ns.route('/')
@ns.response(*doc_resp(BAD_REQUEST))
@ns.response(*doc_resp(UNAUTHORIZED))
class MovieResource(Resource):

    mra_client = MovieRapidAPI()

    @ns.response(*doc_resp(CREATE_RESP))
    @ns.response(*doc_resp(UNAUTHORIZED))
    @ns.response(*doc_resp(DUPLICATED))
    @ns.doc(params=auth_in_header)
    @ns.expect(post_movie_model)
    @required_login(as_admin=True)
    @inject_validated_payload(PostSchema())
    def post(self, payload, token_data):
        try:
            top_cast = payload.pop('top_cast')
            movie_attributes = payload | self.mra_client.movie_factory(payload.get('tag'))
            extra_details = movie_attributes.pop('extra_details')
            Movie(**movie_attributes).db_store()

            movie_id = Movie.get_id_by_tag(payload.get('tag'))
            for actor in top_cast:
                Cast(actor).db_store()
                MovieCast(movie_id, Cast.get_id_by_name(actor)).db_store()

            for genre in extra_details.get('genres'):
                Genre(genre).db_store()
                MovieGenres(movie_id, Genre.get_id_by_genre(genre)).db_store()

            for director in extra_details.get('directors'):
                Cast(director).db_store()
                MovieCast(movie_id, Cast.get_id_by_name(director), True).db_store()

        except SQLDuplicateException as sqe:
            raise sqe
        return CREATE_RESP

    @ns.response(*doc_resp(FETCH_RESP))
    @ns.response(*doc_resp(UNAUTHORIZED))
    @ns.marshal_list_with(get_movie_model)
    @ns.doc(params=auth_in_header)
    @required_login(as_admin=True)
    def get(self, token_data):
        return GetSchema(many=True).dump(build_movies_payload(Movie.fetch_movies()))

    @ns.response(*doc_resp(UPDATE_RESP))
    @ns.expect(put_movie_model)
    @inject_validated_payload(PutSchema())
    @required_login(as_admin=True)
    @ns.doc(params=auth_in_header)
    def put(self, payload):
        Movie.edit_movie(**payload)
        return UPDATE_RESP

    @ns.response(*doc_resp(DELETE_RESP))
    @ns.expect(delete_movie_model)
    @inject_validated_payload(DeleteSchema())
    @required_login(as_admin=True)
    @ns.doc(params=auth_in_header)
    def delete(self, payload, token_data):
        Movie.delete_movies(**payload)
        MovieCast.on_movie_delete(payload.get('id'))
        MovieGenres.on_movie_delete(payload.get('id'))
        return DELETE_RESP


def build_movies_payload(movies):
    def movie_payload(movie):
        return movie.obj_as_dict() | MovieCast.fetch_movie_cast(movie.id) | MovieGenres.fetch_movie_genres(movie.id)
    return list(map(movie_payload, movies))


