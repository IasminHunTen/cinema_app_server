from extra_modules import api
from flask_restx import fields

get_room_model = api.model('GetRoomSchema', {
    'id': fields.String(),
    'name': fields.String(),
    'row_count': fields.Integer(),
    'column_count': fields.Integer()
})

post_room_model = api.model('PostRoomSchema', {
    'name': fields.String(required=True),
    'row_count': fields.Integer(default=20),
    'column_count': fields.Integer(default=20)
})

put_room_model = api.model('PutRoomSchema', {
    'id': fields.String(required=True),
    'name': fields.String(),
    'row_count': fields.Integer(),
    'column_count': fields.Integer()
})

delete_room_model = api.model('DeleteRoomSchema', {
    'id': fields.String(required=True)
})

