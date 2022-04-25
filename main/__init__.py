import os
import sys
from pathlib import Path

from flask import Flask, Blueprint
from flask_admin import Admin
from flask_cors import CORS
from flask_admin.contrib.sqla import ModelView
root_path = Path(__file__).parent.parent
root_path = os.path.join(root_path, 'main')
sys.path.append(root_path)
from controllers import *
from extra_modules import db, api, flask_marshal, mail
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
    CORS(app)
    if os.getenv('FLASK_ENV') == 'development':
        app.config.from_object('config.dev.Config')
    else:
        app.config.from_object('config.prod.Config')

    mail.init_app(app)
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
    admin.add_view(ModelView(Tickets, db.session))
    with app.app_context():
        db.create_all()
    return app




