from flask_restx import Resource
from flask import request

from models import PriceTickets
from models.schedule import *
from serializable import price_tickets_model
from serializable.schedule import *
from constants.req_responses import *
from constants import string_from_query, auth_in_header
from controllers import Tickets
from utils import doc_resp, inject_validated_payload, date_from_string, required_login

ns = api.namespace('schedule')


@ns.response(*doc_resp(BAD_REQUEST))
@ns.route('/')
class ScheduleResource(Resource):

    @ns.response(*doc_resp(CREATE_RESP))
    @ns.response(*doc_resp(UNAUTHORIZED))
    @ns.expect(post_schedule_model)
    @inject_validated_payload(PostSchedule())
    def post(self, payload):
        Schedule(**payload).db_store()
        return CREATE_RESP

    @ns.response(*doc_resp(FETCH_RESP))
    @ns.doc(params=string_from_query('date'))
    @ns.marshal_list_with(get_schedule_model)
    def get(self):
        d = request.args.get('date')
        if d is not None:
            d = date_from_string(d)
        return GetScheduleSchema(many=True).dump(
            Schedule.get_movies_from_one_day(d)
        ), 200

    @ns.response(*doc_resp(UNAUTHORIZED))
    @ns.response(*doc_resp(UPDATE_RESP))
    @ns.doc(params=auth_in_header)
    @ns.expect(edit_schedule_model)
    @ns.marshal_with(price_tickets_model)
    @required_login(as_admin=True)
    @inject_validated_payload(EditSchedule())
    def put(self, token_data, payload):
        if payload.get('tickets_id') is None:
            amount = Schedule.mark_places(**payload.get('schedule_configuration'), marker='t')
            return PriceTickets().dump({
                'amount': amount
            }), 204
        Schedule.mark_places(*Tickets.get_tickets_by_id(payload.get('tickets_id')), marker='t')
        return PriceTickets().dump({
            'amount': 0
        })

    @ns.response(*doc_resp(DELETE_RESP))
    @ns.expect(delete_schedule_model)
    @inject_validated_payload(DeleteScheduleSchema())
    def delete(self, payload):
        Schedule.delete(**payload)
        return DELETE_RESP









