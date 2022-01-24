from extra_modules import api
from flask_restx import Resource


ns = api.namespace('test')

@ns.route('/')
class TestRoute(Resource):

    def get(self):
        return {'test': 'get'}

