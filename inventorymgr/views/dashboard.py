"""Dashboard view."""


from typing import Any

from flask import render_template

from inventorymgr.views.blueprint import views_blueprint


@views_blueprint.route("/")
def dashboard() -> Any:
    """Returns the dashboard view."""
    return render_template("dashboard.html.j2")
