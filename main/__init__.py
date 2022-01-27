from flask import Flask, Blueprint
from extra_modules import api, db
from models import TestModel
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin()


def create_app():
    app = Flask(__name__)
    blueprint = Blueprint('api', __name__, url_prefix='/api/doc')
    api.init_app(blueprint)
    app.register_blueprint(blueprint)
    app.config.from_object('config.dev.Config')
    db.init_app(app)
    admin.init_app(app)
    admin.add_view(ModelView(TestModel, db.session))

    with app.app_context():
        db.create_all()
    return app




