from flask import current_app as app

from extra_modules import db
from utils import uuid_generator
from . import Room, Movie


class Schedule(db.Model):
    id = db.Column(db.String(64), primary_key=True, default=uuid_generator)
    movie_id = db.Column(db.String(64))
    room_id = db.Column(db.String(64))
    sits_left = db.Column(db.Integer())
    sits_configuration = db.Column(db.String(1024))
    day = db.Column(db.Date())
    hour = db.Column(db.Integer())
    minute = db.Column(db.Integer())
    price = db.Column(db.Float())

    def __init__(self, movie_id, room_id, day, hour, minute, price: None):
        self.movie_id = movie_id
        self.room_id = room_id
        self.day = day
        self.hour = hour
        self.minute = minute
        self.sits_left = Room.get_sits_by_id(room_id)
        self.sits_configuration = '0' * self.sits_left
        self.price = price if price else app.config['STANDARD_PRICE']

    def db_store(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete(cls, id):
        program = cls.query.get(id)
        if program is not None:
            db.session.delete(program)
            db.session.commit()

    @classmethod
    def get_movies_from_one_day(cls, date=None):
        if date is None:
            return cls.query.all()
        return cls.query.filter_by(day=date).all()

    @classmethod
    def get_room_availability(cls, room_id, day_date):
        def movie_run(movie):
            start = movie.hour * 60 + movie.minute
            return start, start + Movie.get_run_time_by_id(movie.movie_id) + app.config['GAP_BETWEEN_MOVIES']
        return [movie_run(movie) for movie in cls.query.filter_by(day=day_date).filter_by(room_id=room_id).all()]







