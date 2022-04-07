from flask_restx import fields

from extra_modules import api


ufg_model = api.model('UFGSchema', {
    'genres': fields.List(fields.String())
})
