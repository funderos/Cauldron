from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from ..service.eval_service import get_eval_progress, increment_progress, write_eval_request_log
import json
import uuid
import time

evaluation = Blueprint('evaluation', __name__)


@evaluation.route('/')
def login():
    return render_template("eval/login.html", user=current_user)

@evaluation.route('/tasks')
@login_required
def tasks():
    progress = get_eval_progress(current_user.username)
    if progress > 6:
        return redirect(url_for('evaluation.survey'))
    return render_template("eval/tasks.html", user=current_user, progress=progress)

@evaluation.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    if request.method == 'GET':
        progress = get_eval_progress(current_user.username)
        if progress > 10:
            return redirect(url_for('auth.finish_eval'))
        return render_template("eval/survey.html", user=current_user, progress=progress)
    else:
        req = {'timestamp': time.time(), 'route': '/survey', 'method': 'POST', 'args': request.form}
        write_eval_request_log(current_user.username, req)
        increment_progress(current_user.username)
        return redirect(url_for('evaluation.survey'))