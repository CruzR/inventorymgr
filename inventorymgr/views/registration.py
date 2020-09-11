"""Views concerning registration."""

from typing import Any

from inventorymgr.views.blueprint import views_blueprint


@views_blueprint.route("/register/<token>")
def register(token: str) -> Any:  # pylint: disable=unused-argument
    """Registration form."""
    return views_blueprint.send_static_file("register.html")
