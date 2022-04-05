from split import partition

from extra_modules import db
from utils import debug_print
from . import Cast


class MovieCast(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.String(64))
    cast_member_id = db.Column(db.String(64))
    is_director = db.Column(db.Boolean, default=False)

    def __init__(self, movie_id, cast_member_id, is_director=False):
        self.movie_id = movie_id
        self.cast_member_id = cast_member_id
        self.is_director = is_director

    def db_store(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_movie_cast(cls, movie_id):
        cast = [movie for movie in cls.query.filter_by(movie_id=movie_id).all()]
        directors = filter(lambda x: x.is_director, cast)
        top_cast = filter(lambda x: not x.is_director, cast)
        return {
            'directors': list(map(lambda x: Cast.get_name_by_id(x.cast_member_id), directors)),
            'top_cast': list(map(lambda x: Cast.get_name_by_id(x.cast_member_id), top_cast))
        }

    @classmethod
    def on_movie_delete(cls, movie_id):
        [db.session.delete(movie) for movie in cls.query.filter_by(movie_id=movie_id).all()]

    @classmethod
    def on_cast_delete(cls, member_id):
        [db.session.delete(movie) for movie in cls.query.filter_by(cast_member_id=member_id).all()]





