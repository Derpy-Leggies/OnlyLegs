"""
OnlyLegs - Settings page
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user

blueprint = Blueprint('settings', __name__, url_prefix='/settings')


@blueprint.route('/')
@login_required
def general():
    """
    General settings page
    """
    return render_template('settings/general.html')


@blueprint.route('/server')
@login_required
def server():
    """
    Server settings page
    """
    return render_template('settings/server.html')


@blueprint.route('/account')
@login_required
def account():
    """
    Account settings page
    """
    return render_template('settings/account.html')


@blueprint.route('/logs')
@login_required
def logs():
    """
    Logs settings page
    """
    return render_template('settings/logs.html')
