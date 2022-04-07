from extra_modules import api
from flask_restx import fields

cast_post_model = api.model('PostActorSchema', {
    'name': fields.String(required=True)
})

cast_put_model = api.model('PutActorSchema', {
    'id': fields.String(required=True),
    'name': fields.String(required=True)
})

cast_get_model = api.model('GetActorSchema', {
    'id': fields.String(),
    'name': fields.String()
})

cast_delete_model = api.model('DeleteActorSchema', {
    'id': fields.String(required=True)
})
