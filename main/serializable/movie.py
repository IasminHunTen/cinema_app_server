from extra_modules import api, DictItem

from flask_restx import fields

get_movie_model = api.model('GetMovieSchema', {
    'id': fields.String(),
    'tag': fields.String(),
    'title': fields.String(),
    'plot': fields.String(),
    'year': fields.Integer(),
    'imdb_rate': fields.Float(),
    'run_time': fields.Integer(),
    'poster': fields.String(),
    'trailer': fields.String()
})

post_movie_model = api.model('PostMovieSchema', {
    'tag': fields.String(required=True)
})


put_movie_model = api.model('PutMovieSchema', {
    'id': fields.String(required=True),
    'attributes': DictItem(required=True)
})

delete_movie_model = api.model('DeleteMovieSchema', {
    'id': fields.String(required=True)
})
