import functools
from flask import Blueprint, flash, g, redirect, request, session, url_for, abort, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash

from gallery.db import get_db

from .logger import logger

import re
import uuid

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


# def add_log(code, note=None):    
#     code = int(code)
#     note = str(note)
    
#     user_id = session.get('user_id')
#     user_ip = request.remote_addr
#     db = get_db()
    
#     db.execute(
#         'INSERT INTO logs (ip, user_id, code, note)'
#         ' VALUES (?, ?, ?, ?)',
#         (user_ip, user_id, code, note)
#     )
#     db.commit()


@blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    user_uuid = session.get('uuid')

    if user_id is None or user_uuid is None:
        # This is not needed as the user is not logged in anyway, also spams the logs
        #add_log(103, 'Auth error before app request')
        g.user = None
        session.clear()
    else:
        db = get_db()
        is_alive = db.execute('SELECT * FROM devices WHERE session_uuid = ?',
                              (session.get('uuid'), )).fetchone()

        if is_alive is None:
            logger.add(103, 'Session expired')
            flash(['Session expired!', '3'])
            session.clear()
        else:
            g.user = db.execute('SELECT * FROM users WHERE id = ?',
                                (user_id, )).fetchone()


@blueprint.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    password_repeat = request.form['password-repeat']
    db = get_db()
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
            db.execute(
                'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                (username, email, generate_password_hash(password)),
            )
            db.commit()
        except db.IntegrityError:
            error.append(f"User {username} is already registered!")
        else:
            logger.add(103, f"User {username} registered")
            return 'gwa gwa'

    return jsonify(error)


@blueprint.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    error = None
    user = db.execute('SELECT * FROM users WHERE username = ?',
                      (username, )).fetchone()

    if user is None:
        logger.add(101, f"User {username} does not exist from {request.remote_addr}")
        abort(403)
    elif not check_password_hash(user['password'], password):
        logger.add(102, f"User {username} password error from {request.remote_addr}")
        abort(403)

    try:
        session.clear()
        session['user_id'] = user['id']
        session['uuid'] = str(uuid.uuid4())

        db.execute(
            'INSERT INTO devices (user_id, session_uuid, ip) VALUES (?, ?, ?)',
            (user['id'], session.get('uuid'), request.remote_addr))
        db.commit()
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
    logger.add(103, f"User {g.user['username']} - id: {g.user['id']} logged out")
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
