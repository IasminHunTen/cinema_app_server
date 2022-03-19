from marshmallow import Schema, fields, validate

class GetRoom(Schema):
    id = fields.String()
    name = fields.String()
    sits = fields.Integer()


class PostRoom(Schema):
    name = fields.String(validate=[validate.Length(min=2, max=32)])
    sits = fields.Integer(default=128)


class PutRoom(Schema):
    id = fields.String(required=True)
    name = fields.String(validate=[validate.Length(min=2, max=32)])
    sits = fields.Integer()


class DeleteRoom(Schema):
    id = fields.String(required=True)


