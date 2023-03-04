"""
OnlyLegs - Database
Database models and functions for SQLAlchemy
"""
import os
from datetime import datetime
import platformdirs

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


path_to_db = os.path.join(platformdirs.user_config_dir('onlylegs'), 'gallery.sqlite')
engine = create_engine(f'sqlite:///{path_to_db}', echo=False)
base = declarative_base()


class users (base): # pylint: disable=too-few-public-methods, C0103
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

    posts = relationship('posts')
    groups = relationship('groups')
    session = relationship('sessions')
    log = relationship('logs')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.created_at = datetime.now()


class posts (base): # pylint: disable=too-few-public-methods, C0103
    """
    Post table
    Joins with group_junction
    """
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    file_name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    alt = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, nullable=False)

    junction = relationship('group_junction')

    def __init__(self, file_name, description, alt, author_id):
        self.file_name = file_name
        self.description = description
        self.alt = alt
        self.author_id = author_id
        self.created_at = datetime.now()


class groups (base): # pylint: disable=too-few-public-methods, C0103
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

    junction = relationship('group_junction')

    def __init__(self, name, description, author_id):
        self.name = name
        self.description = description
        self.author_id = author_id
        self.created_at = datetime.now()


class group_junction (base): # pylint: disable=too-few-public-methods, C0103
    """
    Junction table for posts and groups
    Joins with posts and groups
    """
    __tablename__ = 'group_junction'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))

    def __init__(self, group_id, post_id):
        self.group_id = group_id
        self.post_id = post_id


class sessions (base): # pylint: disable=too-few-public-methods, C0103
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

    def __init__(self, user_id, session_uuid, ip_address, user_agent, active): # pylint: disable=too-many-arguments, C0103
        self.user_id = user_id
        self.session_uuid = session_uuid
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.active = active
        self.created_at = datetime.now()


class logs (base): # pylint: disable=too-few-public-methods, C0103
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

    def __init__(self, user_id, ip_address, code, msg):
        self.user_id = user_id
        self.ip_address = ip_address
        self.code = code
        self.msg = msg
        self.created_at = datetime.now()


class bans (base): # pylint: disable=too-few-public-methods, C0103
    """
    Bans table
    """
    __tablename__ = 'bans'

    id = Column(Integer, primary_key=True)
    ip_address = Column(String, nullable=False)
    code = Column(Integer, nullable=False)
    msg = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __init__(self, ip_address, code, msg):
        self.ip_address = ip_address
        self.code = code
        self.msg = msg
        self.created_at = datetime.now()


base.metadata.create_all(engine)
