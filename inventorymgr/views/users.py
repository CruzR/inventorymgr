"Server-side views concerning users."

from typing import Any

from flask import render_template, session
from inventorymgr import service
from inventorymgr.views.blueprint import views_blueprint


@views_blueprint.route("/users")
def users() -> Any:
    """List view of all users."""
    return render_template("users.html.j2", users=service.iterate_users())


@views_blueprint.route("/users/new")
def user_new() -> Any:
    """View for creating new users."""
    return render_template("user_new.html.j2")


@views_blueprint.route("/users/<user_id>")
def user_detail(user_id: str) -> Any:
    """Server-side rendered detail view for users."""
    try:
        parsed_user_id = session["user_id"] if user_id == "me" else int(user_id)
    except ValueError:
        return f"'{user_id}' is not a valid user ID.", 404
    return render_template("user.html.j2", user=service.read_user(parsed_user_id))


@views_blueprint.route("/users/<user_id>/edit")
def user_edit(user_id: str) -> Any:  # pylint: disable=unused-argument
    """View for editing an existing user."""
    return render_template("user_edit.html.j2")
