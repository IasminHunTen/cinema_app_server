from random import choice
from string import digits

from werkzeug.exceptions import BadRequest

from extra_modules import db
from utils import CryptoManager, debug_print


def _generate_card_number():
    return ''.join([choice(digits) for _ in range(16)])


def generate_pk():
    key = _generate_card_number()
    return key if CreditCard.query.get(key) is None else generate_pk()


class CreditCard(db.Model):

    card_number = db.Column(db.String(16), primary_key=True, default=generate_pk)
    holder_id = db.Column(db.String(64))
    expire_year = db.Column(db.Integer)
    expire_month = db.Column(db.Integer)
    sold = db.Column(db.Float)
    encrypted_ccv = db.Column(db.String(128))

    __crypto_man = CryptoManager()

    def __init__(self, holder_id, expire_year, expire_month, ccv, sold=50.0):
        self.holder_id = holder_id
        self.expire_year = expire_year
        self.expire_month = expire_month
        self.encrypted_ccv = self.__crypto_man.encrypt_word(str(ccv))
        self.sold = sold

    def db_store(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_user_credit_cards(cls, user_id):
        return cls.query.filter_by(holder_id=user_id).all()

    @classmethod
    def alter_credit_card_sold(cls, card_number, amount, ccv=None):

        card = cls.query.get(card_number)
        cls.__crypto_man.decrypt_word(card.encrypted_ccv)
        if ccv is not None:
            if str(ccv) != cls.__crypto_man.decrypt_word(card.encrypted_ccv):
                raise BadRequest('Invalid CCV')
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
            db.session.delete(card) for card in cls.query.filer_by(holder_id=user_id).all()
        ]
        db.session.commit()
