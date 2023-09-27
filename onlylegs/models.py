"""
OnlyLegs - Database models and ions for SQLAlchemy
"""
from uuid import uuid4
from flask_login import UserMixin
from onlylegs.extensions import db


class AlbumJunction(db.Model):
    """
    Junction table for picturess and albums
    Joins with picturess and albums
    """

    __tablename__ = "album_junction"

    id = db.Column(db.Integer, primary_key=True)

    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"))
    picture_id = db.Column(db.Integer, db.ForeignKey("pictures.id"))

    date_added = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),  # pylint: disable=E1102
    )


class Pictures(db.Model):
    """
    Pictures table
    """

    __tablename__ = "pictures"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    filename = db.Column(db.String, unique=True, nullable=False)
    mimetype = db.Column(db.String, nullable=False)
    colours = db.Column(db.PickleType, nullable=False)

    description = db.Column(db.String, nullable=False)
    alt = db.Column(db.String, nullable=False)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),  # pylint: disable=E1102
    )

    album_fk = db.relationship("AlbumJunction", backref="pictures")
    exif_fk = db.relationship("Exif", backref="pictures")


class Exif(db.Model):
    """
    Exif data for pictures
    """

    __tablename__ = "exif"

    id = db.Column(db.Integer, primary_key=True)
    picture_id = db.Column(db.Integer, db.ForeignKey("pictures.id"))

    key = db.Column(db.String, nullable=False)
    value = db.Column(db.PickleType, nullable=False)


class Albums(db.Model):
    """
    albums table
    """

    __tablename__ = "albums"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),  # pylint: disable=E1102
    )

    album_fk = db.relationship("AlbumJunction", backref="albums")


class Users(db.Model, UserMixin):
    """
    Users table
    """

    __tablename__ = "users"

    # Gallery used information
    id = db.Column(db.Integer, primary_key=True)
    alt_id = db.Column(db.String, unique=True, nullable=False, default=str(uuid4()))

    picture = db.Column(db.String, default=None)
    colour = db.Column(db.PickleType, default=None)
    banner = db.Column(db.String, default=None)

    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    joined_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),  # pylint: disable=E1102
    )

    pictures_fk = db.relationship("Pictures", backref="author")
    albums_fk = db.relationship("Albums", backref="author")

    def get_id(self):
        return str(self.alt_id)
