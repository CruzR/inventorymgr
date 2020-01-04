"""API endpoints for handling borrow states."""

from typing import Any, Dict
from flask import Blueprint

from inventorymgr.accesscontrol import requires_permissions
from inventorymgr.api.models import BorrowStateSchema
from inventorymgr.auth import authentication_required
from inventorymgr.db.models import BorrowState


bp = Blueprint('borrowstates', __name__, url_prefix='/api/v1/borrowstates')


@bp.route('', methods=('GET',))
@authentication_required
@requires_permissions('manage_checkouts')
def fetch_borrowstates() -> Dict[str, Any]:
    """Fetch all borrowstates."""
    borrowstates = BorrowStateSchema(many=True).dump(BorrowState.query.all())
    return {'borrowstates': borrowstates}
