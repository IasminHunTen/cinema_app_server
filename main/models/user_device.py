from marshmallow import Schema, fields


class GetUserDeviceSchema(Schema):
    devices = fields.List(fields.String())





