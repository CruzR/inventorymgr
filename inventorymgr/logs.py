"""API endpoints for getting checkout / checkin logs."""

from typing import Any, Dict

from flask import Blueprint

from inventorymgr.api.models import LogEntrySchema
from inventorymgr.auth import authentication_required
from inventorymgr.db.models import LogEntry


bp = Blueprint("logs", __name__, url_prefix="/api/v1/logs")


@bp.route("", methods=("GET",))
@authentication_required
def get_logs() -> Dict[str, Any]:
    """API endpoint for getting checkout / checkin logs."""
    return {"logs": LogEntrySchema(many=True).dump(LogEntry.query.all())}
