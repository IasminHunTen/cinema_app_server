from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from datetime import date


class PostCreditCard(Schema):
    expire_year = fields.Integer(required=True)
    expire_month = fields.Integer(required=True, validate=[validate.Range(min=1, max=12)])
    sold = fields.Float()
    ccv = fields.Integer(required=True, validate=[validate.Range(min=100, max=999)])

    @validates_schema
    def custom_validation(self, data, **kwargs):
        today = date.today()
        if data['expire_year'] > today.year:
            return
        elif data['expire_year'] == today.year and data['expire_month'] >= today.month:
            return
        raise ValidationError('Card already expired')


class GetCreditCard(Schema):
    card_number = fields.String()
    sold = fields.Float()
    expire_year = fields.Integer()
    expire_month = fields.Integer()


class EditCreditCardSold(Schema):
    card_number = fields.String(required=True)
    amount = fields.Float(required=True)
    ccv = fields.Integer()
