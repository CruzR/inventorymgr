"""Server-side views for items."""

from typing import Any

from flask import render_template

from inventorymgr.views.blueprint import views_blueprint


@views_blueprint.route("/items")
def items() -> Any:
    """List view for items."""
    return render_template("items.html.j2")


@views_blueprint.route("/items/<item_id>/edit")
def edit_item(item_id: str) -> Any:  # pylint: disable=unused-argument
    """Edit view for items."""
    return render_template("item_edit.html.j2")


@views_blueprint.route("/items/new")
def item_new() -> Any:
    """View for creating new items."""
    return render_template("item_new.html.j2")
