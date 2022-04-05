from flask_restx import fields

from extra_modules import api
from controllers import Movie, Room


class MovieTitleField(fields.Raw):
    def format(self, value):
        return Movie.get_movie_title(value)


class RoomNameField(fields.Raw):
    def format(self, value):
        return Room.get_room_name_by_id(value)


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
    'movie_title': MovieTitleField(attribute='movie_id'),
    'room_name': RoomNameField(attribute='room_id'),
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



