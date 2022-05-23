from extra_modules import db, NotFound
from utils import uuid_generator


class Movie(db.Model):
    id = db.Column(db.String(64), primary_key=True, default=uuid_generator)
    tag = db.Column(db.String(32), unique=True)
    title = db.Column(db.String(64))
    plot = db.Column(db.Text())
    year = db.Column(db.Integer())
    imdb_rate = db.Column(db.Numeric())
    run_time = db.Column(db.Integer())
    poster = db.Column(db.String(1024))
    trailer = db.Column(db.String(1024))
    voting_mode = db.Column(db.Boolean())

    def __init__(self, tag, title, plot, year, imdb_rate, run_time, poster, trailer):
        self.tag = tag
        self.title = title
        self.plot = plot
        self.year = year
        self.imdb_rate = imdb_rate
        self.run_time = run_time
        self.poster = poster
        self.trailer = trailer
        self.voting_mode = False

    def db_store(self):
        db.session.add(self)
        db.session.commit()

    def obj_as_dict(self):
        return {
            'id': self.id,
            'tag': self.tag,
            'title': self.title,
            'plot': self.plot,
            'year': self.year,
            'imdb_rate': self.imdb_rate,
            'run_time': self.run_time,
            'poster': self.poster,
            'trailer': self.trailer
        }

    @classmethod
    def fetch_movies(cls, ids=None, only_votes=False):
        bulk_movies = cls.query
        if only_votes:
            bulk_movies = bulk_movies.filter_by(voting_mode=True)
        if ids is None:
            return bulk_movies.all()
        content = []
        for id in ids:
            movie = bulk_movies.get(id)
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

    @classmethod
    def get_id_by_tag(cls, tag):
        return cls.query.filter_by(tag=tag).first().id

    @classmethod
    def get_run_time_by_id(cls, id):
        return cls.query.get(id).run_time

    @classmethod
    def get_movie_title(cls, id):
        return cls.query.get(id).title

    @classmethod
    def movie_exist(cls, id):
        return id in [movie.id for movie in cls.query.all()]

