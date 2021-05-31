from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import configparser
import os
here = os.path.dirname(__file__)

db = SQLAlchemy()
config = configparser.ConfigParser()
config.read(os.path.join(here, 'config.ini'))

DB_NAME = config['FLASK']['DB_NAME']
SECRET_KEY = config['FLASK']['SECRET_KEY']

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(here, DB_NAME)}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .clustering import clustering

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(clustering, url_prefix='/clustering/')

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
