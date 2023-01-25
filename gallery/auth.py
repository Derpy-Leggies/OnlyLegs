import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from gallery.db import get_db
import re

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()

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
    elif not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
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
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, generate_password_hash(password)),
            )
            db.commit()
        except db.IntegrityError:
            error.append(f"User {username} is already registered!")
        else:
            return 'gwa gwa'
        
    return jsonify(error)


@blueprint.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    error = None
    user = db.execute(
        'SELECT * FROM users WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
        abort(403)
    elif not check_password_hash(user['password'], password):
        abort(403)

    if error is None:
        session.clear()
        session['user_id'] = user['id']
        flash(['Logged in successfully!', '4'])
        return 'gwa gwa'


@blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
