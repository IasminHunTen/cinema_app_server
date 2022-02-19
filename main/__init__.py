from flask import Flask, Blueprint
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .extra_modules import api, db, flask_marshal
from .controllers import User
from .routes import users_ns

admin = Admin()


def create_app():
    app = Flask(__name__)
    blueprint = Blueprint('api', __name__, url_prefix='/api/doc')
    api.init_app(blueprint)
    api.add_namespace(users_ns)
    app.register_blueprint(blueprint)
    app.config.from_object('config.dev.Config')

    db.init_app(app)
    flask_marshal.init_app(app)

    admin.init_app(app)
    admin.add_view(ModelView(User, db.session))
    with app.app_context():
        db.create_all()
    return app




