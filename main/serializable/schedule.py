from flask_restx import fields

from extra_modules import api
from controllers import Movie, Room


post_schedule_model = api.model('PostScheduleSchema', {
    'movie_id': fields.String(required=True),
    'room_id': fields.String(required=True),
    'day': fields.Date(required=True),
    'hour': fields.Integer(required=True),
    'minute': fields.Integer(required=True),
    'price': fields.Float()
})

get_schedule_model = api.model('GetScheduleSchema', {
    'id': fields.String(),
    'movie_id': fields.String(),
    'room_id': fields.String(),
    'day': fields.Date(),
    'hour': fields.Integer(),
    'minute': fields.Integer(),
    'price': fields.Float(),
    'sits_left': fields.Integer(),
    'sits_configuration': fields.String()
})

delete_schedule_model = api.model('DeleteScheduleSchema', {
    'id': fields.String(required=True)
})

schedule_configuration = api.model('ScheduleConfigurationSchema', {
    'schedule_id': fields.String(),
    'configuration': fields.String()
})

edit_schedule_model = api.model('EditScheduleSchema', {
    'schedule_configuration': fields.Nested(schedule_configuration, default={}),
    'tickets_id': fields.String()
})
