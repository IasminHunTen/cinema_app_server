from sqlalchemy.exc import IntegrityError

from extra_modules import db, SQLDuplicateException, NotFound
from utils import uuid_generator


class Genre(db.Model):
    id = db.Column(db.String(64), primary_key=True, default=uuid_generator)
    genre = db.Column(db.String(64), unique=True)

    def __init__(self, genre):
        self.genre = genre

    def db_store(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            pass

    @classmethod
    def fetch(cls, ids=None):
        if ids is None:
            return cls.query.all()
        content = []
        for id in ids:
            genre = cls.query.get(id)
            if genre is None:
                raise NotFound(f'genre with id={id}')
            content.append(genre)
        return content

    @classmethod
    def db_alter(cls, id, genre):
        if cls.query.filter_by(genre=genre).first():
            raise SQLDuplicateException(f"genre '{genre}' already exist")
        db_genre = cls.query.get(id)
        if db_genre is None:
            raise NotFound(f'genre with id={id}')
        db_genre.genre = genre
        db.session.commit()

    @classmethod
    def db_delete(cls, id):
        if cls.query.get(id) is None:
            raise NotFound(f'genre with id={id}')
        db.session.delete(
            cls.query.get(id)
        )
        db.session.commit()

    @classmethod
    def get_id_by_genre(cls, genre):
        return cls.query.filter_by(genre=genre).first().id

    @classmethod
    def get_genre_by_id(cls, id):
        return cls.query.get(id).genre
