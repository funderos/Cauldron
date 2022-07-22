from flask import Blueprint, render_template, send_from_directory
from flask_login import current_user
import configparser
from .. import db
import os
here = os.path.dirname(__file__)

config = configparser.ConfigParser()
config.read(os.path.join(here, '../config.ini'))

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user, eval=int(config['EVAL']['ENABLED']))

@views.route('/favicon.ico') 
def favicon():
    return send_from_directory(os.path.join(views.root_path, '../static'), 'images/logos/favicon.ico', mimetype='image/vnd.microsoft.icon')
