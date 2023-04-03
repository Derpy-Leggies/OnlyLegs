"""
OnlyLegs - Database models and functions for SQLAlchemy
"""
import os
import platformdirs

from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, PickleType)
from sqlalchemy.orm import declarative_base, relationship

from flask_login import UserMixin


USER_DIR = platformdirs.user_config_dir('onlylegs')
DB_PATH = os.path.join(USER_DIR, 'gallery.sqlite')


# In the future, I want to add support for other databases
engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)
base = declarative_base()


class Users (base, UserMixin):  # pylint: disable=too-few-public-methods, C0103
    """
    User table
    Joins with post, groups, session and log
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

    posts = relationship('Posts', backref='users')
    groups = relationship('Groups', backref='users')
    session = relationship('Sessions', backref='users')
    log = relationship('Logs', backref='users')


class Posts (base):  # pylint: disable=too-few-public-methods, C0103
    """
    Post table
    Joins with group_junction
    """
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, nullable=False)

    file_name = Column(String, unique=True, nullable=False)
    file_type = Column(String, nullable=False)

    image_exif = Column(PickleType, nullable=False)
    image_colours = Column(PickleType, nullable=False)

    post_description = Column(String, nullable=False)
    post_alt = Column(String, nullable=False)

    junction = relationship('GroupJunction', backref='posts')


class Groups (base):  # pylint: disable=too-few-public-methods, C0103
    """
    Group table
    Joins with group_junction
    """
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, nullable=False)

    junction = relationship('GroupJunction', backref='groups')


class GroupJunction (base):  # pylint: disable=too-few-public-methods, C0103
    """
    Junction table for posts and groups
    Joins with posts and groups
    """
    __tablename__ = 'group_junction'

    id = Column(Integer, primary_key=True)
    date_added = Column(DateTime, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))


class Sessions (base):  # pylint: disable=too-few-public-methods, C0103
    """
    Session table
    Joins with user
    """
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    session_uuid = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    user_agent = Column(String, nullable=False)
    active = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False)


class Logs (base):  # pylint: disable=too-few-public-methods, C0103
    """
    Log table
    Joins with user
    """
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    ip_address = Column(String, nullable=False)
    code = Column(Integer, nullable=False)
    msg = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)


class Bans (base):  # pylint: disable=too-few-public-methods, C0103
    """
    Bans table
    """
    __tablename__ = 'bans'

    id = Column(Integer, primary_key=True)
    ip_address = Column(String, nullable=False)
    code = Column(Integer, nullable=False)
    msg = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)


# check if database file exists, if not create it
if not os.path.isfile(DB_PATH):
    base.metadata.create_all(engine)
    print('Database created')
