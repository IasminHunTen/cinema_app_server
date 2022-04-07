from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from flask import current_app as app
from datetime import date
from controllers import Movie, Schedule
from utils import tuple_overlap, minutes_2_time


class PostSchedule(Schema):
    movie_id = fields.String(required=True)
    room_id = fields.String(required=True)
    day = fields.Date(required=True)
    hour = fields.Integer(required=True)
    minute = fields.Integer(required=True, validate=[validate.Range(min=0, max=59)])
    price = fields.Integer(default=0)

    @validates_schema
    def custom_validation(self, data, **kwargs):
        if data.get('hour') < app.config['START_HOUR'] or data.get('hour') >= app.config['LIMIT_HOUR']:
            raise ValidationError(f"hour must be between {app.config['START_HOUR']} and {app.config['LIMIT_HOUR']}")
        if date.today() > data.get('day'):
            raise ValidationError(f"A past day can not be use")
        start_time = data.get('hour') * 60 + data.get('minute')
        necessary_time = (start_time,
                          start_time +
                          Movie.get_run_time_by_id(data.get('movie_id')) +
                          app.config['GAP_BETWEEN_MOVIES'])

        for time_stamp in Schedule.get_room_availability(data.get('room_id'), data.get('day')):
            if not tuple_overlap(necessary_time, time_stamp):
                raise ValidationError(f"necessary time for this movie {minutes_2_time(*necessary_time)} "
                                      f"overlaps with other interval {minutes_2_time(*time_stamp)} from the chosen room")


class GetScheduleSchema(Schema):
    id = fields.String()
    movie_id = fields.String()
    room_id = fields.String()
    sits_left = fields.Integer()
    sits_configuration = fields.String()
    day = fields.Date()
    hour = fields.Integer()
    minute = fields.Integer()
    price = fields.Float()


class DeleteScheduleSchema(Schema):
    id = fields.String(required=True)
