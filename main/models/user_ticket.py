from marshmallow import Schema, fields


class BuyTickets(Schema):
    schedule_id = fields.String(required=True)
    sits_configuration = fields.String(required=True)


class RevokeTickets(Schema):
    tickets_id = fields.String(required=True)


class GetUserTickets(Schema):
    id = fields.String()
    schedule_id = fields.String()
    sits_configuration = fields.String()


class PriceTickets(Schema):
    amount = fields.Float()
