"""Server-side views concerning qualifications."""

from typing import Any

from flask import render_template

from inventorymgr.views.blueprint import views_blueprint


@views_blueprint.route("/qualifications/<qualification_id>")
def qualification_detail(
    qualification_id: str,  # pylint: disable=unused-argument
) -> Any:
    """Return a detail view for a qualification."""
    return render_template("qualification_detail.html.j2")
