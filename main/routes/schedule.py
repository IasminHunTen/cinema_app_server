from flask_restx import Resource
from flask import request

from models.schedule import *
from serializable.schedule import *
from constants.req_responses import *
from constants import string_from_query
from utils import doc_resp, inject_validated_payload, date_from_string

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

    @ns.response(*doc_resp(DELETE_RESP))
    @ns.expect(delete_schedule_model)
    @inject_validated_payload(DeleteScheduleSchema())
    def delete(self, payload):
        Schedule.delete(**payload)
        return DELETE_RESP







