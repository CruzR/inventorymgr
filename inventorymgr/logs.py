"""API endpoints for getting checkout / checkin logs."""

from flask import Blueprint, Response, make_response

from inventorymgr import api
from inventorymgr.auth import authentication_required
from inventorymgr.db.models import LogEntry


bp = Blueprint("logs", __name__, url_prefix="/api/v1/logs")


@bp.route("", methods=("GET",))
@authentication_required
def get_logs() -> Response:
    """API endpoint for getting checkout / checkin logs."""
    response = make_response(
        api.LogEntryCollection(logs=list(LogEntry.query.all())).json()
    )
    response.headers["Content-Type"] = "application/json; encoding=utf-8"
    return response
