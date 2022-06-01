from flask_restx import fields

from extra_modules import api

post_card_model = api.model('PostCreditCardSchema', {
    'expire_year': fields.Integer(required=True),
    'expire_month': fields.Integer(required=True),
    'sold': fields.Float(required=True),
    'ccv': fields.Integer(required=True)
})

get_card_model = api.model('GetCreditCardSchema', {
    'card_number': fields.String(),
    'expire_year': fields.Integer(),
    'expire_month': fields.Integer(),
    'sold': fields.Float()
})

edit_card_amount_model = api.model('EditCreditCardAmountSchema', {
    'card_number': fields.String(),
    'amount': fields.Float(),
})

