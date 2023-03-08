"""
OnlyLegs - Authentification
User registration, login and logout and locking access to pages behind a login
"""
import re
import uuid
import logging
from datetime import datetime as dt

import functools
from flask import Blueprint, flash, g, redirect, request, session, url_for, abort, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc

from gallery import db


blueprint = Blueprint('auth', __name__, url_prefix='/auth')
db_session = sessionmaker(bind=db.engine)
db_session = db_session()


def login_required(view):
    """
    Decorator to check if a user is logged in before accessing a page
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or session.get('uuid') is None:
            logging.error('Authentification failed')
            session.clear()
            return redirect(url_for('gallery.index'))

        return view(**kwargs)

    return wrapped_view


@blueprint.before_app_request
def load_logged_in_user():
    """
    Runs before every request and checks if a user is logged in
    """
    user_id = session.get('user_id')
    user_uuid = session.get('uuid')

    if user_id is None or user_uuid is None:
        g.user = None
        session.clear()
    else:
        is_alive = db_session.query(db.Sessions).filter_by(session_uuid=user_uuid).first()

        if is_alive is None:
            logging.info('Session expired')
            flash(['Session expired!', '3'])
            session.clear()
        else:
            g.user = db_session.query(db.Users).filter_by(id=user_id).first()


@blueprint.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    """
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    password_repeat = request.form['password-repeat']

    error = []

    email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    username_regex = re.compile(r'\b[A-Za-z0-9._%+-]+\b')


    if not username or not username_regex.match(username):
        error.append('Username is invalid!')

    if not email or not email_regex.match(email):
        error.append('Email is invalid!')

    if not password:
        error.append('Password is empty!')
    elif len(password) < 8:
        error.append('Password is too short! Longer than 8 characters pls')

    if not password_repeat:
        error.append('Enter password again!')
    elif password_repeat != password:
        error.append('Passwords do not match!')

    if error:
        return jsonify(error)


    try:
        register_user = db.Users(username=username,
                                 email=email,
                                 password=generate_password_hash(password),
                                 created_at=dt.utcnow())
        db_session.add(register_user)
        db_session.commit()
    except exc.IntegrityError:
        return f'User {username} is already registered!'
    except Exception as err:
        logging.error('User %s could not be registered: %s', username, err)
        return 'Something went wrong!'

    logging.info('User %s registered', username)
    return 'gwa gwa'


@blueprint.route('/login', methods=['POST'])
def login():
    """
    Log in a registered user by adding the user id to the session
    """
    username = request.form['username']
    password = request.form['password']

    user = db_session.query(db.Users).filter_by(username=username).first()
    error = []


    if user is None:
        logging.error('User %s does not exist. Login attempt from %s',
                      username, request.remote_addr)
        error.append('Username or Password is incorrect!')
    elif not check_password_hash(user.password, password):
        logging.error('User %s entered wrong password. Login attempt from %s',
                      username, request.remote_addr)
        error.append('Username or Password is incorrect!')

    if error:
        abort(403)


    try:
        session.clear()
        session['user_id'] = user.id
        session['uuid'] = str(uuid.uuid4())

        session_query = db.Sessions(user_id=user.id,
                                   session_uuid=session.get('uuid'),
                                   ip_address=request.remote_addr,
                                   user_agent=request.user_agent.string,
                                   active=True,
                                   created_at=dt.utcnow())

        db_session.add(session_query)
        db_session.commit()
    except Exception as err:
        logging.error('User %s could not be logged in: %s', username, err)
        abort(500)

    logging.info('User %s logged in from %s', username, request.remote_addr)
    flash(['Logged in successfully!', '4'])
    return 'gwa gwa'


@blueprint.route('/logout')
def logout():
    """
    Clear the current session, including the stored user id
    """
    logging.info('User (%s) %s logged out', session.get('user_id'), g.user.username)
    session.clear()
    return redirect(url_for('index'))
