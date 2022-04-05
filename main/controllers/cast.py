from sqlalchemy.exc import IntegrityError

from extra_modules import db, NotFound
from utils import uuid_generator, debug_print


class Cast(db.Model):
    id = db.Column(db.String(64), primary_key=True, default=uuid_generator)
    name = db.Column(db.String(128), unique=True)

    def __init__(self, name):
        self.name = name

    def db_store(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            return

    @classmethod
    def fetch_cast(cls, ids=None):
        if ids is None:
            return cls.query.all()
        content = []
        for id in ids:
            actor = cls.query.get(id)
            if actor is None:
                raise NotFound(f'cast member with id={id}')
            content.append(actor)
        return content

    @classmethod
    def delete_actor(cls, id):
        actor = cls.query.get(id)
        if actor is None:
            raise NotFound(f'cast member with id={id}')
        db.session.delete(actor)
        db.session.commit()

    @classmethod
    def edit_actor(cls, id, name):
        actor = cls.query.get(id)
        if actor is None:
            raise NotFound(f'cast member with id={id}')
        if actor.name == name:
            return
        actor.name = name
        db.session.commit()

    @classmethod
    def get_id_by_name(cls, name):
        return cls.query.filter_by(name=name).first().id

    @classmethod
    def get_name_by_id(cls, id):
        return cls.query.get(id).name















