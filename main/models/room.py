from marshmallow import Schema, fields, validate


class GetRoom(Schema):
    id = fields.String()
    name = fields.String()
    row_count = fields.Integer(default=20)
    column_count = fields.Integer(default=20)


class PostRoom(Schema):
    name = fields.String(validate=[validate.Length(min=2, max=32)])
    row_count = fields.Integer(default=20)
    column_count = fields.Integer(default=20)


class PutRoom(Schema):
    id = fields.String(required=True)
    name = fields.String(validate=[validate.Length(min=2, max=32)])
    row_count = fields.Integer(default=20)
    column_count = fields.Integer(default=20)


class DeleteRoom(Schema):
    id = fields.String(required=True)


