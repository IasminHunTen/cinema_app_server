from werkzeug.exceptions import BadRequest

from extra_modules import db, NotFound, AuthException
from constants import CRED_MAX_LENGTH
from utils import CryptoManager, uuid_generator, generate_number_sequence


class User(db.Model):
    id = db.Column(db.String(64), primary_key=True, default=uuid_generator)
    username = db.Column(db.String(CRED_MAX_LENGTH), unique=True)
    email = db.Column(db.String(CRED_MAX_LENGTH), unique=True)
    password = db.Column(db.String(128))
    isAdmin = db.Column(db.Boolean, default=False)
    revoke_tickets_prejudice = db.Column(db.Float())
    reset_password_code = db.Column(db.String(6))

    __crypto_man = CryptoManager()

    def __init__(self, username, email, password, is_admin=False):
        self.username = username
        self.email = email
        self.password = self.__crypto_man.encrypt_word(password)
        self.isAdmin = is_admin
        self.revoke_tickets_prejudice = 0.0
        self.reset_password_code = None

    def db_store(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def login(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user is None:
            raise NotFound('No user with this username')
        if cls.__crypto_man.decrypt_word(user.password) != password:
            raise AuthException('Wrong Password')
        return user

    @classmethod
    def fetch_users(cls):
        return cls.query.all()

    @classmethod
    def fetch_my_self(cls, id):
        return cls.query.get(id)

    @classmethod
    def update_prejudice(cls, user_id, amount):
        user = cls.query.get(user_id)
        user.revoke_tickets_prejudice += amount
        db.session.commit()

    @classmethod
    def get_user_prejudice(cls, user_id):
        return cls.query.get(user_id).revoke_tickets_prejudice

    @classmethod
    def reset_password(cls, username, new_password, validation_code):
        user = cls.query.filter_by(username=username).first()
        if user.reset_password_code is None:
            raise AuthException('Request for password change was not made')
        if user.reset_password_code != validation_code:
            raise BadRequest('Validation Code does not match')
        user.password = cls.__crypto_man.encrypt_word(new_password)
        user.reset_password_code = None
        db.session.commit()

    @classmethod
    def generate_reset_validation_code(cls, username):
        user = cls.query.filter_by(username=username).first()
        if user is None:
            raise NotFound('No user found with this email')
        user.reset_password_code = generate_number_sequence(6)
        db.session.commit()
        return user

    @classmethod
    def delete_user(cls, id):
        user = cls.query.get(id)
        if user is None:
            raise NotFound('User Not found')
        db.session.delete(user)
        db.session.commit()
