from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
from flask_login import login_user, login_required, logout_user, current_user
from ..service.eval_service import create_eval_file
from datetime import timedelta
import configparser
import uuid
import os
here = os.path.dirname(__file__)

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def home():
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

@auth.route('/starteval')
def start_eval():
    userId = str(uuid.uuid4())
    user = User(username=userId, isRegistered=False, password=generate_password_hash(str(uuid.uuid4()), method='sha256'))
    db.session.add(user)
    db.session.commit()
    flash('Evaluation started successfully!', category='success')
    login_user(user, remember=True)
    create_eval_file(userId)
    return render_template("eval/tasks.html", user=current_user, progress=0)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/finisheval')
@login_required
def finish_eval():
    logout_user()
    return render_template("eval/completed.html", user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/init-users')
def init_users():
    config = configparser.ConfigParser()
    config.read(os.path.join(here, 'config.ini'))
    for username in config['ACCESS']:
        user = User.query.filter_by(username=username).first()
        if not user:
            new_user = User(username=username, isRegistered=True, password=generate_password_hash(
                config['ACCESS'][username], method='sha256'))
            db.session.add(new_user)
            db.session.commit()
    return '<h1>Users created</h1>'