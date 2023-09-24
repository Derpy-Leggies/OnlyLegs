"""
Onlylegs - Image Groups
Why groups? Because I don't like calling these albums
sounds more limiting that it actually is in this gallery
"""
from flask import Blueprint, render_template, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from onlylegs.models import Pictures, Users, AlbumJunction, Albums
from onlylegs.extensions import db
from onlylegs.utils import colour


blueprint = Blueprint("group", __name__, url_prefix="/group")


@blueprint.route("/", methods=["GET"])
def groups():
    """
    Group overview, shows all image groups
    """
    groups = Albums.query.all()

    # For each group, get the 3 most recent images
    for group in groups:
        group.author_username = (
            Users.query.with_entities(Users.username)
            .filter(Users.id == group.author_id)
            .first()[0]
        )

        # Get the 3 most recent images
        images = (
            AlbumJunction.query.with_entities(AlbumJunction.picture_id)
            .filter(AlbumJunction.album_id == group.id)
            .order_by(AlbumJunction.date_added.desc())
            .limit(3)
        )

        # For each image, get the image data and add it to the group item
        group.images = []
        for image in images:
            group.images.append(
                Pictures.query.with_entities(
                    Pictures.filename, Pictures.alt, Pictures.colours, Pictures.id
                )
                .filter(Pictures.id == image[0])
                .first()
            )

    return render_template("list.html", groups=groups)


@blueprint.route("/", methods=["POST"])
@login_required
def groups_post():
    """
    Creates a group
    """
    group_name = request.form.get("name", "").strip()
    group_description = request.form.get("description", "").strip()

    new_group = Albums(
        name=group_name,
        description=group_description,
        author_id=current_user.id,
    )

    db.session.add(new_group)
    db.session.commit()

    flash(["Group created!", "1"])
    return jsonify({"message": "Group created", "id": new_group.id})


@blueprint.route("/<int:group_id>", methods=["GET"])
def group(group_id):
    """
    Group view, shows all images in a group
    """
    # Get the group, if it doesn't exist, 404
    group = db.get_or_404(Albums, group_id, description="Group not found! D:")

    # Get all images in the group from the junction table
    junction = (
        AlbumJunction.query.with_entities(AlbumJunction.picture_id)
        .filter(AlbumJunction.album_id == group_id)
        .order_by(AlbumJunction.date_added.desc())
        .all()
    )

    # Get the image data for each image in the group
    images = []
    for image in junction:
        images.append(Pictures.query.filter(Pictures.id == image[0]).first())

    # Check contrast for the first image in the group for the banner
    text_colour = "rgb(var(--fg-black))"
    if images:
        colour_obj = colour.Colour(images[0].colours[0])
        text_colour = (
            "rgb(var(--fg-black));"
            if colour_obj.is_light()
            else "rgb(var(--fg-white));"
        )

    return render_template(
        "group.html", group=group, images=images, text_colour=text_colour
    )


@blueprint.route("/<int:group_id>", methods=["PUT"])
@login_required
def group_put(group_id):
    """
    Changes the images in a group
    """
    image_id = request.form.get("imageId", "").strip()
    action = request.form.get("action", "").strip()

    group_record = db.get_or_404(Albums, group_id)
    db.get_or_404(Pictures, image_id)  # Check if image exists

    if group_record.author_id != current_user.id:
        return jsonify({"message": "You are not the owner of this group"}), 403

    junction_exist = AlbumJunction.query.filter_by(
        album_id=group_id, picture_id=image_id
    ).first()

    if action == "add" and not junction_exist:
        db.session.add(AlbumJunction(album_id=group_id, picture_id=image_id))
    elif request.form["action"] == "remove":
        AlbumJunction.query.filter_by(album_id=group_id, picture_id=image_id).delete()

    db.session.commit()
    flash(["Group modified!", "1"])
    return jsonify({"message": "Group modified"})


@blueprint.route("/<int:group_id>", methods=["DELETE"])
@login_required
def group_delete(group_id):
    """
    Deletes a group
    """
    group_record = db.get_or_404(Albums, group_id)

    if group_record.author_id != current_user.id:
        return jsonify({"message": "You are not the owner of this group"}), 403

    AlbumJunction.query.filter_by(album_id=group_id).delete()
    db.session.delete(group_record)
    db.session.commit()

    flash(["Group yeeted!", "1"])
    return jsonify({"message": "Group deleted"})


@blueprint.route("/<int:group_id>/<int:image_id>")
def group_post(group_id, image_id):
    """
    Image view, shows the image and its metadata from a specific group
    """
    # Get the image, if it doesn't exist, 404
    image = db.get_or_404(Pictures, image_id, description="Image not found :<")

    # Get all groups the image is in
    groups = (
        AlbumJunction.query.with_entities(AlbumJunction.album_id)
        .filter(AlbumJunction.picture_id == image_id)
        .all()
    )

    # Get the group data for each group the image is in
    image.groups = []
    for group in groups:
        image.groups.append(
            Albums.query.with_entities(Albums.id, Albums.name)
            .filter(Albums.id == group[0])
            .first()
        )

    # Get the next and previous images in the group
    next_url = (
        AlbumJunction.query.with_entities(AlbumJunction.picture_id)
        .filter(AlbumJunction.album_id == group_id)
        .filter(AlbumJunction.picture_id > image_id)
        .order_by(AlbumJunction.date_added.asc())
        .first()
    )
    prev_url = (
        AlbumJunction.query.with_entities(AlbumJunction.picture_id)
        .filter(AlbumJunction.album_id == group_id)
        .filter(AlbumJunction.picture_id < image_id)
        .order_by(AlbumJunction.date_added.desc())
        .first()
    )

    # If there is a next or previous image, get the URL for it
    if next_url:
        next_url = url_for("group.group_post", group_id=group_id, image_id=next_url[0])
    if prev_url:
        prev_url = url_for("group.group_post", group_id=group_id, image_id=prev_url[0])

    close_tab = True
    if request.cookies.get("image-info") == "0":
        close_tab = False

    return render_template(
        "image.html",
        image=image,
        next_url=next_url,
        prev_url=prev_url,
        close_tab=close_tab,
    )
