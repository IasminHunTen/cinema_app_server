from flask import Flask, Blueprint
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from controllers import *
from extra_modules import db, api, flask_marshal
from routes import users_ns, casts_ns, genres_ns, rooms_ns, movies_ns, schedule_ns

admin = Admin()


def create_app():
    app = Flask(__name__)
    blueprint = Blueprint('api', __name__, url_prefix='/api/doc')
    api.init_app(blueprint)
    api.add_namespace(users_ns)
    api.add_namespace(casts_ns)
    api.add_namespace(genres_ns)
    api.add_namespace(rooms_ns)
    api.add_namespace(movies_ns)
    api.add_namespace(schedule_ns)
    app.register_blueprint(blueprint)
    app.config.from_object('config.dev.Config')

    db.init_app(app)
    flask_marshal.init_app(app)

    admin.init_app(app)
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Genre, db.session))
    admin.add_view(ModelView(Room, db.session))
    admin.add_view(ModelView(Cast, db.session))
    admin.add_view(ModelView(Movie, db.session))
    admin.add_view(ModelView(MovieCast, db.session))
    admin.add_view(ModelView(MovieGenres, db.session))
    admin.add_view(ModelView(Schedule, db.session))
    admin.add_view(ModelView(UserDevices, db.session))
    admin.add_view(ModelView(UserFavoriteGenres, db.session))
    admin.add_view(ModelView(CreditCard, db.session))
    with app.app_context():
        db.create_all()
    return app




