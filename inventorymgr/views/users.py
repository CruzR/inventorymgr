"Server-side views concerning users."

from typing import Any

from flask import render_template
from inventorymgr.views.blueprint import views_blueprint


@views_blueprint.route("/users")
def users() -> Any:
    """List view of all users."""
    return render_template("users.html.j2")


@views_blueprint.route("/users/new")
def user_new() -> Any:
    """View for creating new users."""
    return render_template("user_new.html.j2")


@views_blueprint.route("/users/<user_id>")
def user_detail(user_id: str) -> Any:  # pylint: disable=unused-argument
    """Server-side rendered detail view for users."""
    return render_template("user.html.j2")


@views_blueprint.route("/users/<user_id>/edit")
def user_edit(user_id: str) -> Any:  # pylint: disable=unused-argument
    """View for editing an existing user."""
    return render_template("user_edit.html.j2")
