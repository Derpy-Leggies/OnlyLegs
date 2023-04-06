"""
Onlylegs Gallery - Index view
"""
from flask import Blueprint, render_template, request
from werkzeug.exceptions import abort

from sqlalchemy.orm import sessionmaker
from gallery import db


blueprint = Blueprint('gallery', __name__)
db_session = sessionmaker(bind=db.engine)
db_session = db_session()


@blueprint.route('/')
def index():
    """
    Home page of the website, shows the feed of the latest images
    """
    images = db_session.query(db.Posts.filename,
                              db.Posts.alt,
                              db.Posts.colours,
                              db.Posts.created_at,
                              db.Posts.id).order_by(db.Posts.id.desc()).all()

    if request.args.get('coffee') == 'please':
        abort(418)

    return render_template('index.html', images=images)
