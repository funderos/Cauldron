from flask import Blueprint, render_template, request, jsonify, redirect, url_for, make_response
from flask_login import login_required, current_user
from ..service.player_service import get_network, get_ego_ids, get_count_ids
from ..service.cluster_service import get_clustering, get_elbow, get_categorized_stat_fields, get_statistics, get_csv, get_stat_field_tooltips
from ..service.eval_service import get_eval_progress, increment_progress, write_eval_request_log
import json
import time

clustering = Blueprint('clustering', __name__)


@clustering.route('/')
@login_required
def _clustering():
    progress = -1
    if not current_user.isRegistered:
        write_eval_request_log(current_user.username, {'timestamp': time.time(), 'route': '/', 'method': 'GET'})
        progress = get_eval_progress(current_user.username)
    return render_template("clustering.html",
    user=current_user, egoids = get_ego_ids(), idcount = get_count_ids(),
    statfields = get_categorized_stat_fields(), progress = progress)

@clustering.route('/network/<puuid>')
@login_required
def network(puuid):
    print(puuid)
    res = get_network(puuid, request.args)
    if not current_user.isRegistered:
        req = {'timestamp': time.time(), 'route': '/network/' + puuid, 'method': 'GET', 'args': request.args}
        write_eval_request_log(current_user.username, req)
    return res

@clustering.route('/cluster')
@login_required
def cluster():
    res = get_clustering(request.args)
    if not current_user.isRegistered:
        req = {'timestamp': time.time(), 'route': '/cluster', 'method': 'GET', 'args': request.args}
        write_eval_request_log(current_user.username, req)
    return res

@clustering.route('/elbow')
@login_required
def elbow():
    res = get_elbow(request.args)
    if not current_user.isRegistered:
        req = {'timestamp': time.time(), 'route': '/elbow', 'method': 'GET', 'args': request.args}
        write_eval_request_log(current_user.username, req)
    return res

@clustering.route('/stats', methods=['GET', 'POST'])
@login_required
def home():
    if not current_user.isRegistered:
            req = {'timestamp': time.time(), 'route': '/stats', 'method': request.method}
            write_eval_request_log(current_user.username, req)
    if request.method == 'GET':
        res = get_statistics()
        return jsonify(res)
    else:
        response = make_response(get_csv(request.json))
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        response.headers["Content-Type"] = "text/csv"
        return response

@clustering.route('/finishtask', methods=['POST'])
@login_required
def finish_task():
    if not current_user.isRegistered:
        req = {'timestamp': time.time(), 'route': '/finishtask', 'method': 'POST', 'args': request.form}
        write_eval_request_log(current_user.username, req)
        increment_progress(current_user.username)
        return redirect(url_for('evaluation.tasks'))
    else:
        return redirect(url_for('views.home'))