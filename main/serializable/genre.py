from extra_modules import api
from flask_restx import fields

genre_post_model = api.model('PostGenreSchema', {
    'genre': fields.String(required=True)
})

genre_put_model = api.model('PutGenreSchema', {
    'id': fields.String(required=True),
    'genre': fields.String(required=True)
})

genre_get_model = api.model('GetGenreSchema', {
    'id': fields.String(),
    'genre': fields.String(),
})

genre_delete_model = api.model('DeleteGenreSchema', {
    'id': fields.String(required=True)
})
