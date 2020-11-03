"""Server-side views for items."""

from typing import Any

from flask import render_template

from inventorymgr.views.blueprint import views_blueprint


@views_blueprint.route("/items")
def items() -> Any:
    """List view for items."""
    return render_template("items.html.j2")
