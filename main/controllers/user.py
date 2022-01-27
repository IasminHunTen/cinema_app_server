from extra_modules import db
from constants import USERNAME_MAX_LENGTH
import uuid


class User(db.Model):
    id = db.Column(db.String(128), primary_key=True, default=str(uuid.uuid4))
    username = db.Column(db.String(USERNAME_MAX_LENGTH),
                         nullable=False,
                         unique=True)
    password = db.Column(db.String(128), nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)
