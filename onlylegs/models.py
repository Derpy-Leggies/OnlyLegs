"""
OnlyLegs - Database models and ions for SQLAlchemy
"""
from uuid import uuid4
from flask_login import UserMixin
from onlylegs.extensions import db


class GroupJunction(db.Model):  # pylint: disable=too-few-public-methods, C0103
    """
    Junction table for posts and groups
    Joins with posts and groups
    """

    __tablename__ = "group_junction"

    id = db.Column(db.Integer, primary_key=True)

    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))

    date_added = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),  # pylint: disable=E1102
    )


class Post(db.Model):  # pylint: disable=too-few-public-methods, C0103
    """
    Post table
    """

    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    filename = db.Column(db.String, unique=True, nullable=False)
    mimetype = db.Column(db.String, nullable=False)
    exif = db.Column(db.PickleType, nullable=False)
    colours = db.Column(db.PickleType, nullable=False)

    description = db.Column(db.String, nullable=False)
    alt = db.Column(db.String, nullable=False)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),  # pylint: disable=E1102
    )

    junction = db.relationship("GroupJunction", backref="posts")


class Group(db.Model):  # pylint: disable=too-few-public-methods, C0103
    """
    Group table
    """

    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),  # pylint: disable=E1102
    )

    junction = db.relationship("GroupJunction", backref="groups")


class User(db.Model, UserMixin):  # pylint: disable=too-few-public-methods, C0103
    """
    User table
    """

    __tablename__ = "user"

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

    posts = db.relationship("Post", backref="author")
    groups = db.relationship("Group", backref="author")

    def get_id(self):
        return str(self.alt_id)
