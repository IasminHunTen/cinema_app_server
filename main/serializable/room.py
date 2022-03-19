from extra_modules import api
from flask_restx import fields

get_room_model = api.model('GetRoomSchema', {
    'id': fields.String(),
    'name': fields.String(),
    'sits': fields.Integer()
})

post_room_model = api.model('PostRoomSchema', {
    'name': fields.String(required=True),
    'sits': fields.Integer(required=True, default=128)
})

put_room_model = api.model('PutRoomSchema', {
    'id': fields.String(required=True),
    'name': fields.String(),
    'sits': fields.Integer()
})

delete_room_model = api.model('DeleteRoomSchema', {
    'id': fields.String(required=True)
})

