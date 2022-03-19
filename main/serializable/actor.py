from extra_modules import api
from flask_restx import fields

actor_post_model = api.model('PostActorSchema', {
    'name': fields.String(required=True)
})

actor_put_model = api.model('PutActorSchema', {
    'id': fields.String(required=True),
    'name': fields.String(required=True)
})

actor_get_model = api.model('GetActorSchema', {
    'id': fields.String(),
    'name': fields.String(),
    'counter': fields.Integer()
})

actor_delete_model = api.model('DeleteActorSchema', {
    'id': fields.String(required=True)
})
