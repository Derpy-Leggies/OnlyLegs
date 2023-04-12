"""
OnlyLegs - Authentication
User registration, login and logout and locking access to pages behind a login
"""
import re
import logging

from flask import Blueprint, flash, redirect, request, url_for, abort, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from flask_login import login_user, logout_user, login_required

from gallery.extensions import db
from gallery.models import User


blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@blueprint.route("/login", methods=["POST"])
def login():
    """
    Log in a registered user by adding the user id to the session
    """
    error = []

    username = request.form["username"].strip()
    password = request.form["password"].strip()
    remember = bool(request.form["remember-me"])

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        logging.error("Login attempt from %s", request.remote_addr)
        error.append("Username or Password is incorrect!")

    if error:
        abort(403)

    login_user(user, remember=remember)

    logging.info("User %s logged in from %s", username, request.remote_addr)
    flash(["Logged in successfully!", "4"])
    return "ok", 200


@blueprint.route("/register", methods=["POST"])
def register():
    """
    Register a new user
    """
    error = []

    # Thanks Fennec for reminding me to strip out the whitespace lol
    username = request.form["username"].strip()
    email = request.form["email"].strip()
    password = request.form["password"].strip()
    password_repeat = request.form["password-repeat"].strip()

    email_regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    username_regex = re.compile(r"\b[A-Za-z0-9._-]+\b")

    # Validate the form
    if not username or not username_regex.match(username):
        error.append("Username is invalid!")

    if not email or not email_regex.match(email):
        error.append("Email is invalid!")

    if not password:
        error.append("Password is empty!")
    elif len(password) < 8:
        error.append("Password is too short! Longer than 8 characters pls")

    if not password_repeat:
        error.append("Enter password again!")
    elif password_repeat != password:
        error.append("Passwords do not match!")

    user_exists = User.query.filter_by(username=username).first()
    if user_exists:
        error.append("User already exists!")

    # If there are errors, return them
    if error:
        print(error)
        return jsonify(error), 400

    register_user = User(
        username=username,
        email=email,
        password=generate_password_hash(password, method="sha256"),
    )
    db.session.add(register_user)
    db.session.commit()

    logging.info("User %s registered", username)
    return "ok", 200


@blueprint.route("/logout")
@login_required
def logout():
    """
    Clear the current session, including the stored user id
    """
    logout_user()
    flash(["Goodbye!!!", "4"])
    return redirect(url_for("gallery.index"))
