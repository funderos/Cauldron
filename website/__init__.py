from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from datetime import timedelta
import configparser
import os
here = os.path.dirname(__file__)

db = SQLAlchemy()
config = configparser.ConfigParser()
config.read(os.path.join(here, 'config/config.ini'))

DB_NAME = config['FLASK']['DB_NAME']
SECRET_KEY = config['FLASK']['SECRET_KEY']

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    #app.config["SESSION_PERMANENT"] = False
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=60)
    app.config["REMEMBER_COOKIE_REFRESH_EACH_REQUEST"] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(here, DB_NAME)}'
    db.init_app(app)

    from .blueprint.views import views
    from .blueprint.auth import auth
    from .blueprint.clustering import clustering
    from .blueprint.evaluation import evaluation

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(clustering, url_prefix='/clustering/')
    app.register_blueprint(evaluation, url_prefix='/eval/')

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.session_protection = "strong"

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
