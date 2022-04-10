from flask_restx import fields

from extra_modules import api

buy_tickets_model = api.model('BuyTicketsSchema', {
    'schedule_id': fields.String(required=True),
    'sits_configuration': fields.String(required=True)
})

revoke_tickets_model = api.model('RevokeTicketsSchema', {
    'tickets_id': fields.String(required=True)
})

get_tickets_model = api.model('GetUserTickets', {
    'id': fields.String(),
    'schedule_id': fields.String(),
    'sits_configuration': fields.String()
})

buy_tickets_response = api.model('', {
    'tickets_id': fields.String(),
    'amount': fields.Float()
})

price_tickets_model = api.model('', {
    'amount': fields.Float()
})
