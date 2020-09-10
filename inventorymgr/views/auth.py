"""Views concerning authentication."""

from typing import Any

from inventorymgr.views.blueprint import views_blueprint


@views_blueprint.route("/login")
def login() -> Any:
    """Login form view."""
    return views_blueprint.send_static_file("login.html")
