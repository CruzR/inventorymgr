"""API endpoints for handling borrow states."""

import datetime
from typing import Any, Dict, Iterable, cast

from flask import Blueprint, request

from inventorymgr.accesscontrol import requires_permissions
from inventorymgr.api.models import (BorrowStateSchema, CheckinRequestSchema,
                                     CheckoutRequestSchema)
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


@bp.route('/checkin', methods=('POST',))
@authentication_required
@requires_permissions('manage_checkouts')
def checkin() -> Dict[str, Any]:
    """API endpoint for checkin of borrowed items."""
    checkin_request = CheckinRequestSchema().load(request.json)
    now = _utcnow()
    borrowstates = []
    for item_id in checkin_request['item_ids']:
        for borrow_state in open_borrowstates_for_item(item_id):
            borrow_state.returned_at = now
            borrowstates.append(borrow_state)
    db.session.commit()
    return {'borrowstates': BorrowStateSchema(many=True).dump(borrowstates)}


def open_borrowstates_for_item(item_id: int) -> Iterable[BorrowState]:
    """Return all borrow states for an item without a return date."""
    return cast(
        Iterable[BorrowState],
        BorrowState.query.filter_by(borrowed_item_id=item_id, returned_at=None))
