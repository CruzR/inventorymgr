"Server-side views concerning users."

from typing import Any

from flask import render_template
from inventorymgr.views.blueprint import views_blueprint


@views_blueprint.route("/users/<user_id>")
def user_detail(user_id: str) -> Any:  # pylint: disable=unused-argument
    """Server-side rendered detail view for users."""
    return render_template("user.html.j2")
