from flask import Flask, Blueprint
from extra_modules import api
from routes.route_for_test import ns as test_route


def create_app():
    app = Flask(__name__)
    blueprint = Blueprint('api', __name__, url_prefix='/api/doc')
    api.init_app(blueprint)
    app.register_blueprint(blueprint)

    api.add_namespace(test_route)

    app.config.from_object('config.dev.Config')
    return app




