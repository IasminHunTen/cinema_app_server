from marshmallow import Schema, fields


class UFGSchema(Schema):
    genres = fields.List(fields.String())
