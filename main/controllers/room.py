import re

from extra_modules import db, NotFound
from utils import uuid_generator


def name_generator():
    rooms = Room.query.all()
    if not len(rooms):
        return 'room1'
    for room in rooms[::-1]:
        if re.match(r'^room[0-9]+$', room.name):
            last_index = int(room.name[4:])
            last_index += 1
            return f'room{last_index}'
    return 'room1'


class Room(db.Model):
    id = db.Column(db.String(64), primary_key=True, default=uuid_generator)
    name = db.Column(db.String(64), unique=True, default=name_generator)
    sits = db.Column(db.Integer(), default=128)

    def __init__(self, name, sits):
        self.name = name
        self.sits = sits

    def db_store(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_all(cls):
        return cls.query.all()

    @classmethod
    def alter_room(cls, id, name=None, sits=None):
        room = cls.query.get(id)
        if room is None:
            raise NotFound(f'room with id={id}')
        if name:
            room.name = name
        if sits:
            room.sits = sits
        db.session.commit()

    @classmethod
    def delete_room(cls, id):
        room = cls.query.get(id)
        if room is None:
            raise NotFound(f'room with id={id}')
        db.session.delete(room)
        db.session.commit()

    @classmethod
    def get_sits_by_id(cls, id):
        return cls.query.get(id).sits

    @classmethod
    def get_room_name_by_id(cls, id):
        return cls.query.get(id).name














