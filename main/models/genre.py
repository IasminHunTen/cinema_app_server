from marshmallow import Schema, fields, validate


class GetGenres(Schema):
    id = fields.String()
    genre = fields.String()


class PostGenre(Schema):
    genre = fields.String(required=True, validate=[validate.Length(min=2, max=64)])


class PutGenre(Schema):
    id = fields.String(required=True)
    genre = fields.String(required=True, validate=[validate.Length(min=2, max=64)])


class DeleteGenre(Schema):
    id = fields.String(required=True)


