from werkzeug.exceptions import BadRequest

from extra_modules import db
from utils import uuid_generator, debug_print
from . import Schedule


class Tickets(db.Model):
    id = db.Column(db.String(64), primary_key=True, default=uuid_generator)
    schedule_id = db.Column(db.String(64))
    user_id = db.Column(db.String(64))
    sits_configuration = db.Column(db.String(64))

    def __init__(self, schedule_id, user_id, sits_configuration):
        self.schedule_id = schedule_id
        self.user_id = user_id
        self.sits_configuration = sits_configuration

    def db_store(self):
        amount = Schedule.mark_places(self.schedule_id, self.sits_configuration, 'r')
        db.session.add(self)
        db.session.commit()
        return self.id, amount

    @classmethod
    def get_user_tickets(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_tickets_by_id(cls, tickets_id):
        tickets = cls.query.get(tickets_id)
        if tickets is None:
            raise BadRequest('Tickets not found')
        return tickets.schedule_id, tickets.sits_configuration

    @classmethod
    def revoke_order(cls, tickets_id):
        tickets = cls.query.get(tickets_id)
        amount = Schedule.mark_places(tickets.schedule_id, tickets.sits_configuration, 'f')
        db.session.delete(tickets)
        db.session.commit()
        return amount












