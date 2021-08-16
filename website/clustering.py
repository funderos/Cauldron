from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, make_response
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from .player_service import get_network, get_ego_ids, get_count_ids
from .cluster_service import get_clustering, get_elbow, get_categorized_stat_fields, get_statistics, get_csv
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import json

clustering = Blueprint('clustering', __name__)


@clustering.route('/')
@login_required
def _clustering():
    return render_template("clustering.html",
    user=current_user, egoids = get_ego_ids(), idcount = get_count_ids(),
    statfields = get_categorized_stat_fields() )

@clustering.route('/network/<puuid>')
@login_required
def network(puuid):
    return jsonify(get_network(puuid, request.args))

@clustering.route('/cluster')
@login_required
def cluster():
    return get_clustering(request.args)
    #return jsonify(get_clustering(request.args))

@clustering.route('/elbow')
@login_required
def elbow():
    return get_elbow(request.args)

@clustering.route('/stats', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'GET':
        return jsonify(get_statistics())
    else:
        response = make_response(get_csv(request.json))
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        response.headers["Content-Type"] = "text/csv"
        return response