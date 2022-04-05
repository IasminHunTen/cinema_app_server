from sqlalchemy import ForeignKey

from extra_modules import db
from . import Genre

class MovieGenres(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.String(64))
    genre_id = db.Column(db.String(64))

    def __init__(self, movie_id, genre_id):
        self.movie_id = movie_id
        self.genre_id = genre_id

    def db_store(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_movie_genres(cls, movie_id):
        return {
            'genres': [Genre.get_genre_by_id(genre.genre_id) for genre in cls.query.filter_by(movie_id=movie_id).all()]
        }

    @classmethod
    def fetch_all_movie_from_genre(cls, genre_id):
        return [movie.id for movie in cls.query.filter_by(genre_id=genre_id).all()]

    @classmethod
    def on_movie_delete(cls, movie_id):
        [db.session.delete(movie) for movie in cls.query.filter_by(movie_id=movie_id).all()]

    @classmethod
    def on_genre_delete(cls, genre_id):
        [db.session.delete(movie) for movie in cls.query.filter_by(genre_id=genre_id).all()]


