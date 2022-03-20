from marshmallow import Schema, fields, validate


class PostCast(Schema):
    name = fields.String(required=True, validate=[validate.Length(min=3)])


class PutCast(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True, validate=[validate.Length(min=3)])


class GetCast(Schema):
    id = fields.String()
    name = fields.String()


class DeleteActor(Schema):
    id = fields.String()







