from extra_modules import db, NotFound
from utils import uuid_generator, debug_print


class Cast(db.Model):
    id = db.Column(db.String(64), primary_key=True, default=uuid_generator)
    name = db.Column(db.String(128))

    def __init__(self, name):
        self.name = name

    def db_store(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_actors(cls, ids=None):
        if ids is None:
            return cls.query.all()
        content = []
        for id in ids:
            actor = cls.query.get(id)
            if actor is None:
                raise NotFound(f'actor with id={id}')
            content.append(actor)
        return content

    @classmethod
    def delete_actor(cls, id):
        actor = cls.query.get(id)
        if actor is None:
            raise NotFound(f'actor with id={id}')
        db.session.delete(actor)
        db.session.commit()

    @classmethod
    def edit_actor(cls, id, name):
        actor = cls.query.get(id)
        if actor is None:
            raise NotFound(f'actor with id={id}')
        if actor.name == name:
            return
        actor.name = name
        db.session.commit()















