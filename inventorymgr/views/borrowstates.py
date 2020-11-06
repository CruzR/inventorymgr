"""Views for manipulating borrow states."""

from typing import Any

from flask import render_template

from inventorymgr.views.blueprint import views_blueprint


@views_blueprint.route("/borrowstates")
def borrowstates_list() -> Any:
    """Return a list view of active borrow states."""
    return render_template("borrowstates.html.j2")


@views_blueprint.route("/checkout")
def borrowstates_checkout() -> Any:
    """View that allows checkout of items."""
    return render_template("borrowstates_checkout.html.j2")
