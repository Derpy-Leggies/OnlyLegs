"""
Onlylegs - API endpoints
"""
from flask import Blueprint, flash, jsonify, request
from flask_login import login_required, current_user

from onlylegs.extensions import db
from onlylegs.models import Post, Group, GroupJunction


blueprint = Blueprint("group_api", __name__, url_prefix="/api/group")


@blueprint.route("/create", methods=["POST"])
@login_required
def create_group():
    """
    Creates a group
    """
    new_group = Group(
        name=request.form["name"],
        description=request.form["description"],
        author_id=current_user.id,
    )

    db.session.add(new_group)
    db.session.commit()

    return jsonify({"message": "Group created", "id": new_group.id})


@blueprint.route("/modify", methods=["POST"])
@login_required
def modify_group():
    """
    Changes the images in a group
    """
    group_id = request.form["group"]
    image_id = request.form["image"]
    action = request.form["action"]

    group = db.get_or_404(Group, group_id)
    db.get_or_404(Post, image_id)  # Check if image exists

    if group.author_id != current_user.id:
        return jsonify({"message": "You are not the owner of this group"}), 403

    if (action == "add" and not GroupJunction.query.filter_by(group_id=group_id, post_id=image_id).first()):
        db.session.add(GroupJunction(group_id=group_id, post_id=image_id))
    elif request.form["action"] == "remove":
        GroupJunction.query.filter_by(group_id=group_id, post_id=image_id).delete()

    db.session.commit()
    return jsonify({"message": "Group modified"})


@blueprint.route("/delete", methods=["POST"])
def delete_group():
    """
    Deletes a group
    """
    group_id = request.form["group"]
    group = db.get_or_404(Group, group_id)

    if group.author_id != current_user.id:
        return jsonify({"message": "You are not the owner of this group"}), 403

    GroupJunction.query.filter_by(group_id=group_id).delete()
    db.session.delete(group)
    db.session.commit()

    flash(["Group yeeted!", "1"])
    return jsonify({"message": "Group deleted"})
