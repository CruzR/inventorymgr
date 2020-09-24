"""Views concerning registration."""

from typing import Any

from flask import render_template

from inventorymgr.views.blueprint import views_blueprint


@views_blueprint.route("/register/<token>")
def register(token: str) -> Any:  # pylint: disable=unused-argument
    """Registration form."""
    return views_blueprint.send_static_file("register.html")


@views_blueprint.route("/tokens")
def tokens() -> Any:
    """List view of registration tokens."""
    return render_template("tokens.html.j2")
