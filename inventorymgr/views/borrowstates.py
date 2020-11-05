"""Views for manipulating borrow states."""

from typing import Any

from flask import render_template

from inventorymgr.views.blueprint import views_blueprint


@views_blueprint.route("/borrowstates")
def borrowstates_list() -> Any:
    """Return a list view of active borrow states."""
    return render_template("borrowstates.html.j2")
