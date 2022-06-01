import datetime
import random

from werkzeug.exceptions import BadRequest

from extra_modules import db
from utils import CryptoManager, generate_number_sequence


def generate_pk():
    key = generate_number_sequence(16)
    return key if CreditCard.query.get(key) is None else generate_pk()


class CreditCard(db.Model):

    card_number = db.Column(db.String(16), primary_key=True, default=generate_pk)
    holder_id = db.Column(db.String(64))
    expire_year = db.Column(db.Integer)
    expire_month = db.Column(db.Integer)
    sold = db.Column(db.Float)
    encrypted_ccv = db.Column(db.String(128))

    __crypto_man = CryptoManager()

    def __init__(self, holder_id):
        today = datetime.date.today()
        self.holder_id = holder_id
        self.expire_year = today.year + 2
        self.expire_month = today.month
        self.encrypted_ccv = random.randint(100, 999)
        self.sold = 200

    def db_store(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_user_credit_cards(cls, user_id):
        return cls.query.filter_by(holder_id=user_id).all()

    @classmethod
    def alter_credit_card_sold(cls, card_number, amount):
        card = cls.query.get(card_number)
        if card.sold + amount < 0:
            raise BadRequest(f'Insufficient founds, in order to pay: {amount}')
        card.sold += amount
        db.session.commit()

    @classmethod
    def delete_user_credit_card(cls, card_number):
        db.session.delete(
            cls.query.get(card_number)
        )
        db.session.commit()

    @classmethod
    def on_user_delete(cls, user_id):
        [
            db.session.delete(card) for card in cls.query.filter_by(holder_id=user_id).all()
        ]
        db.session.commit()
