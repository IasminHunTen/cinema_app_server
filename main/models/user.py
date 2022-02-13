from marshmallow import Schema, fields, validate, ValidationError
from string import ascii_lowercase, ascii_uppercase, whitespace

from ..constants import CRED_MIN_LENGTH, CRED_MAX_LENGTH, \
    CRED_OUT_OF_BOUNDS, PASSWORD_WITH_WHITESPACES, PASSWORD_WITHOUT_LOWERCASE, PASSWORD_WITHOUT_UPPERCASE
from ..utils import str_inter


def validate_cred(cred):
    if not (CRED_MIN_LENGTH <= len(cred) <= CRED_MAX_LENGTH):
        raise ValidationError(CRED_OUT_OF_BOUNDS)


def validate_password(password):
    validate_cred(password)
    if not str_inter(password, ascii_uppercase):
        raise ValidationError(PASSWORD_WITHOUT_UPPERCASE)
    if not str_inter(password, ascii_lowercase):
        raise ValidationError(PASSWORD_WITHOUT_LOWERCASE)
    if str_inter(password, whitespace):
        raise ValidationError(PASSWORD_WITH_WHITESPACES)


class UserPost(Schema):
    username = fields.String(required=True,
                             validate=validate_cred)
    email = fields.String(required=True, validate=[validate.Email(), validate.Length(max=CRED_MAX_LENGTH)])
    password = fields.String(required=True,
                             validate=validate_password)
    isAdmin = fields.Boolean(default=False)


class GetUsers(Schema):
    id = fields.String()
    username = fields.String()
    email = fields.String()

