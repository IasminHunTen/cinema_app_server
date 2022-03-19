import re

from extra_modules import db
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
    sits = db.Column(db.Integer())

    def __init__(self, name, sits):
        self.name = name
        self.sits = sits

    def store_room(self):
        db.session.add(self)
        db.session.commit()

    def fetch_all(self):
        return self.query.all()

    def fetch_by_id(self, room_id):
        return self.query.get(room_id)

    def alter_room(self, room_id, name=None, sits=None):
        room = self.query.get(room_id)
        if name:
            self.name = name
        if sits:
            self.sits = sits
        db.session.commit()

    def delete_room(self, room_id):
        db.session.delete(
            self.query.get(room_id)
        )
        db.session.commit()













