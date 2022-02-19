from uuid import uuid4

from ..extra_modules import db
from ..constants import CRED_MAX_LENGTH
from ..utils import CryptoManager


class User(db.Model):
    id = db.Column(db.String(32), primary_key=True, default=str(uuid4()))
    username = db.Column(db.String(CRED_MAX_LENGTH),
                         nullable=False,
                         unique=True)
    email = db.Column(db.String(CRED_MAX_LENGTH), unique=True)
    password = db.Column(db.String(128), nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)

    __crypto_man = CryptoManager()

    def __init__(self, username, email, password, is_admin=False):
        self.username = username
        self.email = email
        self.password = self.__crypto_man.encrypt_word(password)
        self.isAdmin = is_admin

    def db_store(self):
        db.session.add(self)
        db.session.commit()









