"""
Onlylegs - Image Groups
Why groups? Because I don't like calling these albums
sounds more limiting that it actually is in this gallery
"""
from flask import Blueprint, render_template, url_for

from onlylegs.models import Post, User, GroupJunction, Group
from onlylegs.extensions import db
from onlylegs.utils import contrast


blueprint = Blueprint("group", __name__, url_prefix="/group")


@blueprint.route("/", methods=["GET"])
def groups():
    """
    Group overview, shows all image groups
    """
    groups = Group.query.all()

    # For each group, get the 3 most recent images
    for group in groups:
        group.author_username = (
            User.query.with_entities(User.username)
            .filter(User.id == group.author_id)
            .first()[0]
        )

        # Get the 3 most recent images
        images = (
            GroupJunction.query.with_entities(GroupJunction.post_id)
            .filter(GroupJunction.group_id == group.id)
            .order_by(GroupJunction.date_added.desc())
            .limit(3)
        )

        # For each image, get the image data and add it to the group item
        group.images = []
        for image in images:
            group.images.append(
                Post.query.with_entities(Post.filename, Post.alt, Post.colours, Post.id)
                .filter(Post.id == image[0])
                .first()
            )

    return render_template("list.html", groups=groups)


@blueprint.route("/<int:group_id>")
def group(group_id):
    """
    Group view, shows all images in a group
    """
    # Get the group, if it doesn't exist, 404
    group = db.get_or_404(Group, group_id, description="Group not found! D:")

    # Get all images in the group from the junction table
    junction = (
        GroupJunction.query.with_entities(GroupJunction.post_id)
        .filter(GroupJunction.group_id == group_id)
        .order_by(GroupJunction.date_added.desc())
        .all()
    )

    # Get the image data for each image in the group
    images = []
    for image in junction:
        images.append(Post.query.filter(Post.id == image[0]).first())

    # Check contrast for the first image in the group for the banner
    text_colour = "rgb(var(--fg-black))"
    if images:
        text_colour = contrast.contrast(
            images[0].colours[0], "rgb(var(--fg-black))", "rgb(var(--fg-white))"
        )

    return render_template(
        "group.html", group=group, images=images, text_colour=text_colour
    )


@blueprint.route("/<int:group_id>/<int:image_id>")
def group_post(group_id, image_id):
    """
    Image view, shows the image and its metadata from a specific group
    """
    # Get the image, if it doesn't exist, 404
    image = db.get_or_404(Post, image_id, description="Image not found :<")

    # Get all groups the image is in
    groups = (
        GroupJunction.query.with_entities(GroupJunction.group_id)
        .filter(GroupJunction.post_id == image_id)
        .all()
    )

    # Get the group data for each group the image is in
    image.groups = []
    for group in groups:
        image.groups.append(
            Group.query.with_entities(Group.id, Group.name)
            .filter(Group.id == group[0])
            .first()
        )

    # Get the next and previous images in the group
    next_url = (
        GroupJunction.query.with_entities(GroupJunction.post_id)
        .filter(GroupJunction.group_id == group_id)
        .filter(GroupJunction.post_id > image_id)
        .order_by(GroupJunction.date_added.asc())
        .first()
    )
    prev_url = (
        GroupJunction.query.with_entities(GroupJunction.post_id)
        .filter(GroupJunction.group_id == group_id)
        .filter(GroupJunction.post_id < image_id)
        .order_by(GroupJunction.date_added.desc())
        .first()
    )

    # If there is a next or previous image, get the URL for it
    if next_url:
        next_url = url_for("group.group_post", group_id=group_id, image_id=next_url[0])
    if prev_url:
        prev_url = url_for("group.group_post", group_id=group_id, image_id=prev_url[0])

    return render_template(
        "image.html", image=image, next_url=next_url, prev_url=prev_url
    )
