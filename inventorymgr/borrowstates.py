"""API endpoints for handling borrow states."""

import datetime
from typing import Any, Dict

from flask import Blueprint, request

from inventorymgr.accesscontrol import requires_permissions
from inventorymgr.api.models import BorrowStateSchema, CheckoutRequestSchema
from inventorymgr.auth import authentication_required
from inventorymgr.db import db
from inventorymgr.db.models import BorrowState


bp = Blueprint('borrowstates', __name__, url_prefix='/api/v1/borrowstates')


_utcnow = datetime.datetime.utcnow # pylint: disable=invalid-name


@bp.route('', methods=('GET',))
@authentication_required
@requires_permissions('manage_checkouts')
def fetch_borrowstates() -> Dict[str, Any]:
    """Fetch all borrowstates."""
    borrowstates = BorrowStateSchema(many=True).dump(BorrowState.query.all())
    return {'borrowstates': borrowstates}


@bp.route('/checkout', methods=('POST',))
@authentication_required
@requires_permissions('manage_checkouts')
def checkout() -> Dict[str, Any]:
    """API endpoint to checkout a list of items to a user."""
    checkout_request = CheckoutRequestSchema().load(request.json)
    now = _utcnow()

    borrowstates = [
        BorrowState(
            borrowing_user_id=checkout_request['borrowing_user_id'],
            borrowed_item_id=item_id,
            received_at=now)
        for item_id in checkout_request['borrowed_item_ids']
    ]

    for borrow_state in borrowstates:
        db.session.add(borrow_state)
    db.session.commit()

    return {'borrowstates': BorrowStateSchema(many=True).dump(borrowstates)}
