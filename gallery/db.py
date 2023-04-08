"""
OnlyLegs - Database models and ions for SQLAlchemy
"""
from uuid import uuid4
import os
import platformdirs

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    PickleType,
    func,
)
from sqlalchemy.orm import declarative_base, relationship
from flask_login import UserMixin


USER_DIR = platformdirs.user_config_dir("onlylegs")
DB_PATH = os.path.join(USER_DIR, "instance", "gallery.sqlite3")


# In the future, I want to add support for other databases
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
base = declarative_base()


class Users(base, UserMixin):  # pylint: disable=too-few-public-methods, C0103
    """
    User table
    Joins with post, groups, session and log
    """

    __tablename__ = "users"

    # Gallery used information
    id = Column(Integer, primary_key=True)
    alt_id = Column(String, unique=True, nullable=False, default=str(uuid4()))
    profile_picture = Column(String, nullable=True, default=None)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    joined_at = Column(
        DateTime, nullable=False, server_default=func.now()  # pylint: disable=E1102
    )

    posts = relationship("Posts", backref="users")
    groups = relationship("Groups", backref="users")
    log = relationship("Logs", backref="users")

    def get_id(self):
        return str(self.alt_id)


class Posts(base):  # pylint: disable=too-few-public-methods, C0103
    """
    Post table
    Joins with group_junction
    """

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(
        DateTime, nullable=False, server_default=func.now()  # pylint: disable=E1102
    )
    filename = Column(String, unique=True, nullable=False)
    mimetype = Column(String, nullable=False)
    exif = Column(PickleType, nullable=False)
    colours = Column(PickleType, nullable=False)
    description = Column(String, nullable=False)
    alt = Column(String, nullable=False)

    junction = relationship("GroupJunction", backref="posts")


class Groups(base):  # pylint: disable=too-few-public-methods, C0103
    """
    Group table
    Joins with group_junction
    """

    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(
        DateTime, nullable=False, server_default=func.now()  # pylint: disable=E1102
    )

    junction = relationship("GroupJunction", backref="groups")


class GroupJunction(base):  # pylint: disable=too-few-public-methods, C0103
    """
    Junction table for posts and groups
    Joins with posts and groups
    """

    __tablename__ = "group_junction"

    id = Column(Integer, primary_key=True)
    date_added = Column(
        DateTime, nullable=False, server_default=func.now()  # pylint: disable=E1102
    )
    group_id = Column(Integer, ForeignKey("groups.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))


class Logs(base):  # pylint: disable=too-few-public-methods, C0103
    """
    Log table
    Joins with user
    """

    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ip_address = Column(String, nullable=False)
    code = Column(Integer, nullable=False)
    note = Column(String, nullable=False)
    created_at = Column(
        DateTime, nullable=False, server_default=func.now()  # pylint: disable=E1102
    )


class Bans(base):  # pylint: disable=too-few-public-methods, C0103
    """
    Bans table
    """

    __tablename__ = "bans"

    id = Column(Integer, primary_key=True)
    ip_address = Column(String, nullable=False)
    code = Column(Integer, nullable=False)
    note = Column(String, nullable=False)
    banned_at = Column(
        DateTime, nullable=False, server_default=func.now()  # pylint: disable=E1102
    )


# check if database file exists, if not create it
if not os.path.isfile(DB_PATH):
    base.metadata.create_all(engine)
    print("Database created")
