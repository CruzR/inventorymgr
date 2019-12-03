"""Defines a catch-all flask view for returning the SPA."""

from typing import Any

from flask import Blueprint, current_app


bp = Blueprint('app', __name__)


@bp.route('/', defaults={'path': ''})
@bp.route('/<path:path>')
def single_page_application(path: str) -> Any:
    """Catch-all flask view for returning the SPA."""
    # pylint: disable=unused-argument
    return current_app.send_static_file('index.html')
