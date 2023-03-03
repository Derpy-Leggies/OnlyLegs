import functools
from flask import Blueprint, flash, g, redirect, request, session, url_for, abort, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash

from gallery import db
from sqlalchemy.orm import sessionmaker
db_session = sessionmaker(bind=db.engine)
db_session = db_session()

from .logger import logger

import re
import uuid

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    user_uuid = session.get('uuid')

    if user_id is None or user_uuid is None:
        # This is not needed as the user is not logged in anyway, also spams the server logs with useless data
        #add_log(103, 'Auth error before app request')
        g.user = None
        session.clear()
    else:
        is_alive = db_session.query(db.sessions).filter_by(session_uuid=user_uuid).first()

        if is_alive is None:
            logger.add(103, 'Session expired')
            flash(['Session expired!', '3'])
            session.clear()
        else:
            g.user = db_session.query(db.users).filter_by(id=user_id).first()
            

@blueprint.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    password_repeat = request.form['password-repeat']
    error = []

    if not username:
        error.append('Username is empty!')

    if not email:
        error.append('Email is empty!')
    elif not re.match(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
        error.append('Email is invalid!')

    if not password:
        error.append('Password is empty!')
    elif len(password) < 8:
        error.append('Password is too short! Longer than 8 characters pls')

    if not password_repeat:
        error.append('Password repeat is empty!')
    elif password_repeat != password:
        error.append('Passwords do not match!')

    if not error:
        try:
            tr = db.users(username, email, generate_password_hash(password))
            db_session.add(tr)
            db_session.commit()
        except Exception as e:
            error.append(f"User {username} is already registered!")
        else:
            logger.add(103, f"User {username} registered")
            return 'gwa gwa'

    return jsonify(error)


@blueprint.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    error = None
    user = db_session.query(db.users).filter_by(username=username).first()

    if user is None:
        logger.add(101, f"User {username} does not exist from {request.remote_addr}")
        abort(403)
    elif not check_password_hash(user.password, password):
        logger.add(102, f"User {username} password error from {request.remote_addr}")
        abort(403)

    try:
        session.clear()
        session['user_id'] = user.id
        session['uuid'] = str(uuid.uuid4())
        
        tr = db.sessions(user.id, session.get('uuid'), request.remote_addr, request.user_agent.string, 1)
        db_session.add(tr)
        db_session.commit()
    except error as err:
        logger.add(105, f"User {username} auth error: {err}")
        abort(500)

    if error is None:
        logger.add(100, f"User {username} logged in from {request.remote_addr}")
        flash(['Logged in successfully!', '4'])
        return 'gwa gwa'

    abort(500)


@blueprint.route('/logout')
def logout():
    logger.add(103, f"User {g.user.username} - id: {g.user.id} logged out")
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or session.get('uuid') is None:
            logger.add(103, "Auth error")
            session.clear()
            return redirect(url_for('gallery.index'))

        return view(**kwargs)

    return wrapped_view
