from flask_restx import Resource
from flask import request

from constants import auth_in_query, string_from_query
from constants.req_responses import *
from extra_modules import SQLDuplicateException
from utils import doc_resp, inject_validated_payload, required_login, MovieRapidAPI
from models.movie import *
from serializable.movie import *
from controllers import Movie, Cast, Genre, MovieGenres, MovieCast, MovieVotes

ns = api.namespace('movies')


@ns.route('/')
@ns.response(*doc_resp(BAD_REQUEST))
@ns.response(*doc_resp(UNAUTHORIZED))
class MovieResource(Resource):

    mra_client = MovieRapidAPI()

    @ns.response(*doc_resp(CREATE_RESP))
    @ns.response(*doc_resp(UNAUTHORIZED))
    @ns.response(*doc_resp(DUPLICATED))
    @ns.doc(params=auth_in_query)
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
                cast_id = Cast(actor).db_store()
                MovieCast(movie_id, cast_id).db_store()

            for genre in extra_details.get('genres'):
                genre_id = Genre(genre).db_store()
                MovieGenres(movie_id, genre_id).db_store()

            for director in extra_details.get('directors'):
                cast_id = Cast(director).db_store()
                MovieCast(movie_id, cast_id, True).db_store()

        except SQLDuplicateException as sqe:
            raise sqe
        return CREATE_RESP

    @ns.response(*doc_resp(FETCH_RESP))
    @ns.response(*doc_resp(UNAUTHORIZED))
    @ns.marshal_list_with(get_movie_model)
    @ns.doc(params=string_from_query('ids'))
    def get(self):
        ids = request.args.get('ids')
        if ids is not None:
            ids = ids.split()
        return GetSchema(many=True).dump(build_movies_payload(Movie.fetch_movies(ids=ids))), 200

    @ns.response(*doc_resp(UPDATE_RESP))
    @ns.expect(put_movie_model)
    @ns.doc(params=auth_in_query)
    @inject_validated_payload(PutSchema())
    @required_login(as_admin=True)
    def put(self, payload, token_data):
        Movie.edit_movie(**payload)
        if 'voting_mode' in payload.get('attributes') and not payload.get('attributes').get('voting_mode'):
            MovieVotes.on_movie_delete(payload.get('id'))
        return UPDATE_RESP

    @ns.response(*doc_resp(DELETE_RESP))
    @ns.expect(delete_movie_model)
    @ns.doc(params=auth_in_query)
    @inject_validated_payload(DeleteSchema())
    @required_login(as_admin=True)
    def delete(self, payload, token_data):
        Movie.delete_movies(**payload)
        MovieCast.on_movie_delete(payload.get('id'))
        MovieGenres.on_movie_delete(payload.get('id'))
        MovieVotes.on_movie_delete(payload.get('id'))
        return DELETE_RESP


@ns.route('/voting')
class MovieVotesResource(Resource):

    @ns.response(*doc_resp(FETCH_RESP))
    @ns.response(*doc_resp(UNAUTHORIZED))
    @ns.marshal_list_with(get_movie_model)
    @ns.doc(params=auth_in_query)
    @required_login(as_admin=True)
    def get(self, token_data):
        return GetSchema(many=True).dump(build_movies_payload(Movie.fetch_movies(only_votes=True))), 200


@ns.route('/voting/count')
class MovieVotingCount(Resource):
    @ns.response(*doc_resp(UNAUTHORIZED))
    @ns.response(*doc_resp(FETCH_RESP))
    @ns.response(*doc_resp(NOT_FOUND))
    @ns.doc(params=auth_in_query)
    @ns.marshal_list_with(get_movie_votes_model)
    @required_login(as_admin=True)
    def get(self, token_data):
        movie_votes = []
        for movie in Movie.fetch_movies(only_votes=True):
            movie_votes.append({
                'movie_id': movie.id,
                'votes': MovieVotes.fetch_votes(movie_id=movie.id)
            })
        return GetMovieVotes(many=True).dump(movie_votes), 200


def build_movies_payload(movies):
    def movie_payload(movie):
        return movie.obj_as_dict() | MovieCast.fetch_movie_cast(movie.id) | MovieGenres.fetch_movie_genres(movie.id)
    return list(map(movie_payload, movies))


