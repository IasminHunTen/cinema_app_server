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
    row_count = db.Column(db.Integer(), default=20)
    column_count = db.Column(db.Integer(), default=20)

    def __init__(self, name, row_count, column_count):
        self.name = name
        self.row_count = row_count
        self.column_count = column_count

    def db_store(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_all(cls):
        return cls.query.all()

    @classmethod
    def alter_room(cls, id, name=None, row_count=None, column_count=None):
        room = cls.query.get(id)
        if room is None:
            raise NotFound(f'room with id={id}')
        if name is not None:
            room.name = name
        if row_count is not None:
            room.row_count = row_count
        if column_count is not None:
            room.column_count = column_count
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
        room = cls.query.get(id)
        return room.row_count * room.column_count

    @classmethod
    def get_room_name_by_id(cls, id):
        return cls.query.get(id).name














