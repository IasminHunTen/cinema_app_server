from marshmallow import Schema, fields, validate


class PostActor(Schema):
    name = fields.String(required=True, validate=[validate.Length(min=3)])


class PutActor(PostActor):
    id = fields.String(required=True)
    name = fields.String(required=True)


class GetActor(Schema):
    id = fields.String()
    name = fields.String()
    counter = fields.Integer()


class DeleteActor(Schema):
    id = fields.String()







