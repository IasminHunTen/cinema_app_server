from extra_modules import db, NotFound
from utils import uuid_generator, debug_print


class Movie(db.Model):
    id = db.Column(db.String(64), primary_key=True, default=uuid_generator)
    tag = db.Column(db.String(32), unique=True)
    title = db.Column(db.String(64))
    plot = db.Column(db.String(2048))
    year = db.Column(db.Integer())
    imdb_rate = db.Column(db.Numeric())
    run_time = db.Column(db.Integer())
    poster = db.Column(db.String(1024))
    trailer = db.Column(db.String(1024))

    def __init__(self, tag, title, plot, year, imdb_rate, run_time, poster, trailer):
        self.tag = tag
        self.title = title
        self.plot = plot
        self.year = year
        self.imdb_rate = imdb_rate
        self.run_time = run_time
        self.poster = poster
        self.trailer = trailer

    def db_store(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_movies(cls, ids=None):
        if ids is None:
            return cls.query.all()
        content = []
        for id in ids:
            movie = cls.query.get(id)
            if movie is None:
                raise NotFound(f'movie with id={id}')
            content.append(movie)
        return content

    @classmethod
    def edit_movie(cls, id, attributes):
        movie = cls.query.get(id)
        if movie is None:
            raise NotFound(f'movie with id={id}')
        for k, v in attributes.items():
            exec(f'movie.{k} = {v}')
        db.session.commit()

    @classmethod
    def delete_movies(cls, id):
        movie = cls.query.get(id)
        if movie is None:
            raise NotFound(f'movie with id={id}')
        db.session.delete(movie)
        db.session.commit()








