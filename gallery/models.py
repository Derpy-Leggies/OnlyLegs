"""
OnlyLegs - Database models and ions for SQLAlchemy
"""
from uuid import uuid4

from flask_login import UserMixin
from .extensions import db


class Users(db.Model, UserMixin):  # pylint: disable=too-few-public-methods, C0103
    """
    User table
    Joins with post, groups, session and log
    """

    __tablename__ = "users"

    # Gallery used information
    id = db.Column(db.Integer, primary_key=True)
    alt_id = db.Column(db.String, unique=True, nullable=False, default=str(uuid4()))
    profile_picture = db.Column(db.String, nullable=True, default=None)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    joined_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),  # pylint: disable=E1102
    )

    posts = db.relationship("Posts", backref="users")
    groups = db.relationship("Groups", backref="users")
    log = db.relationship("Logs", backref="users")

    def get_id(self):
        return str(self.alt_id)


class Posts(db.Model):  # pylint: disable=too-few-public-methods, C0103
    """
    Post table
    Joins with group_junction
    """

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),  # pylint: disable=E1102
    )
    filename = db.Column(db.String, unique=True, nullable=False)
    mimetype = db.Column(db.String, nullable=False)
    exif = db.Column(db.PickleType, nullable=False)
    colours = db.Column(db.PickleType, nullable=False)
    description = db.Column(db.String, nullable=False)
    alt = db.Column(db.String, nullable=False)

    junction = db.relationship("GroupJunction", backref="posts")


class Groups(db.Model):  # pylint: disable=too-few-public-methods, C0103
    """
    Group table
    Joins with group_junction
    """

    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),  # pylint: disable=E1102
    )

    junction = db.relationship("GroupJunction", backref="groups")


class GroupJunction(db.Model):  # pylint: disable=too-few-public-methods, C0103
    """
    Junction table for posts and groups
    Joins with posts and groups
    """

    __tablename__ = "group_junction"

    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),  # pylint: disable=E1102
    )
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))


class Logs(db.Model):  # pylint: disable=too-few-public-methods, C0103
    """
    Log table
    Joins with user
    """

    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    ip_address = db.Column(db.String, nullable=False)
    code = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),  # pylint: disable=E1102
    )


class Bans(db.Model):  # pylint: disable=too-few-public-methods, C0103
    """
    Bans table
    """

    __tablename__ = "bans"

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String, nullable=False)
    code = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String, nullable=False)
    banned_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),  # pylint: disable=E1102
    )
