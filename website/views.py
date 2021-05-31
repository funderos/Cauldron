from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from .player_service import get_network, get_ego_ids
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import json
import os

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
#@login_required
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.isRegistered:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template("home.html", user=current_user)

@views.route('/favicon.ico') 
def favicon():
    return send_from_directory(os.path.join(views.root_path, 'static'), 'images/logos/favicon.ico', mimetype='image/vnd.microsoft.icon')