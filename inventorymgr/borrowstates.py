"""API endpoints for handling borrow states."""

import datetime
from typing import Any, Dict, Iterable, Tuple, cast

from flask import Blueprint, request

from inventorymgr.accesscontrol import requires_permissions
from inventorymgr.api.models import (
    BorrowStateSchema,
    CheckinRequestSchema,
    CheckoutRequestSchema,
)
from inventorymgr.auth import authentication_required
from inventorymgr.db import db
from inventorymgr.db.models import BorrowableItem, BorrowState, LogEntry, User


bp = Blueprint("borrowstates", __name__, url_prefix="/api/v1/borrowstates")


_utcnow = datetime.datetime.utcnow  # pylint: disable=invalid-name


@bp.route("", methods=("GET",))
@authentication_required
@requires_permissions("manage_checkouts")
def fetch_borrowstates() -> Dict[str, Any]:
    """Fetch all borrowstates."""
    borrowstates = BorrowStateSchema(many=True).dump(BorrowState.query.all())
    return {"borrowstates": borrowstates}


@bp.route("/checkout", methods=("POST",))
@authentication_required
@requires_permissions("manage_checkouts")
def checkout() -> Tuple[Dict[str, Any], int]:
    """API endpoint to checkout a list of items to a user."""
    checkout_request = CheckoutRequestSchema().load(request.json)
    now = _utcnow()

    borrowing_user = User.query.get(checkout_request["borrowing_user_id"])
    if borrowing_user is None:
        return {"reason": "no_such_user"}, 400

    borrowed_items = [
        BorrowableItem.query.get(item_id)
        for item_id in checkout_request["borrowed_item_ids"]
    ]

    if any(item is None for item in borrowed_items):
        return {"reason": "nonexistent_item"}, 400

    unqualified_for = [
        item
        for item in borrowed_items
        if not has_required_qualifications(borrowing_user, item)
    ]

    if unqualified_for:
        return {"reason": "missing_qualifications"}, 403

    if any_item_already_borrowed(borrowed_items):
        return {"reason": "already_borrowed"}, 400

    borrowstates = [
        BorrowState(borrowing_user=borrowing_user, borrowed_item=item, received_at=now)
        for item in borrowed_items
    ]

    for borrow_state in borrowstates:
        db.session.add(borrow_state)

    db.session.add(
        LogEntry(
            action="checkout",
            timestamp=now,
            subject=borrowing_user,
            items=borrowed_items,
        )
    )
    db.session.commit()

    return {"borrowstates": BorrowStateSchema(many=True).dump(borrowstates)}, 200


@bp.route("/checkin", methods=("POST",))
@authentication_required
@requires_permissions("manage_checkouts")
def checkin() -> Dict[str, Any]:
    """API endpoint for checkin of borrowed items."""
    checkin_request = CheckinRequestSchema().load(request.json)
    now = _utcnow()
    returning_user = User.query.get(checkin_request["user_id"])
    returned_items = [
        BorrowableItem.query.get(item_id) for item_id in checkin_request["item_ids"]
    ]
    borrowstates = []
    for item in returned_items:
        for borrow_state in open_borrowstates_for_item(item):
            borrow_state.returned_at = now
            borrowstates.append(borrow_state)
    db.session.add(
        LogEntry(
            action="checkin",
            timestamp=now,
            subject=returning_user,
            items=returned_items,
        )
    )
    db.session.commit()
    return {"borrowstates": BorrowStateSchema(many=True).dump(borrowstates)}


def open_borrowstates_for_item(item: BorrowableItem) -> Iterable[BorrowState]:
    """Return all borrow states for an item without a return date."""
    return cast(
        Iterable[BorrowState],
        BorrowState.query.filter_by(borrowed_item=item, returned_at=None).all(),
    )


def has_required_qualifications(user: User, item: BorrowableItem) -> bool:
    """Check if user has all required qualifications to borrow item."""
    return all(q in user.qualifications for q in item.required_qualifications)


def any_item_already_borrowed(items: Iterable[BorrowableItem]) -> bool:
    """Check if any item in item_ids already has an open borrowstate."""
    return any(bool(open_borrowstates_for_item(item)) for item in items)
