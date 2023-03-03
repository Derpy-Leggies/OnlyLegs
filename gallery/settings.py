from flask import Blueprint, render_template, url_for
from werkzeug.exceptions import abort

from gallery.auth import login_required

from datetime import datetime


now = datetime.now()
blueprint = Blueprint('settings', __name__, url_prefix='/settings')


@blueprint.route('/')
@login_required
def general():
    return render_template('settings/general.html')

@blueprint.route('/server')
@login_required
def server():
    return render_template('settings/server.html')

@blueprint.route('/account')
@login_required
def account():
    return render_template('settings/account.html')

@blueprint.route('/logs')
@login_required
def logs():
    return render_template('settings/logs.html')