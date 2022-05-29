"""API endpoints for handling borrow states."""

import datetime
import itertools
from typing import Any, Dict, Iterable, Sequence, Tuple, cast

from flask import Blueprint, request
from sqlalchemy import func
from sqlalchemy import distinct

from inventorymgr.accesscontrol import requires_permissions
from inventorymgr.api.models import (
    BorrowStateSchema,
    CheckinRequestSchema,
    CheckoutRequestSchema,
    ItemCountSchema,
)
from inventorymgr.auth import authentication_required
from inventorymgr.db import db
from inventorymgr.db.models import (
    BorrowableItem,
    BorrowState,
    LogEntry,
    TransferRequest,
    User,
)


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
        BorrowableItem.query.get(elem["id"])
        for elem in checkout_request["borrowed_item_ids"]
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

    quantities = list(map(lambda elem: elem["count"], checkout_request["borrowed_item_ids"]))

    already_borrowed = any_item_already_borrowed(borrowed_items, quantities)
    if already_borrowed:
        items = ItemCountSchema(many=True).dump([{"id": item.id, "count": item.quantity_in_stock} for item, count in already_borrowed])
        return {"reason": "already_borrowed", "items": items}, 400

    borrowstates = [
        BorrowState(borrowing_user=borrowing_user, borrowed_item=item, quantity=qty, received_at=now)
        for item, qty in zip(borrowed_items, quantities)
    ]

    for borrow_state in borrowstates:
        db.session.add(borrow_state)
        borrow_state.borrowed_item.quantity_in_stock -= borrow_state.quantity

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


def try_identify_borrowstates(returning_user, item, quantity):
    open_borrowstate_count = BorrowState.query.with_entities(func.sum(BorrowState.quantity)).filter_by(borrowed_item=item, returned_at=None).scalar()
    distinct_user_count = BorrowState.query.with_entities(func.count(distinct(BorrowState.borrowing_user_id))).filter_by(borrowed_item=item, returned_at=None).scalar()
    if open_borrowstate_count == quantity or distinct_user_count == 1:
        # successfully identified
        return open_borrowstates_for_item(item)#, 0
    #open_borrowstate_count_of_user = BorrowState.query.with_entities(func.sum(BorrowState.quantity)).filter_by(borrowed_item=item, returned_at=None, borrowing_user=returning_user)
    # Otherwise, prefer returning user
    return BorrowState.query.filter_by(borrowed_item=item, returned_at=None, borrowing_user=returning_user).all()#, max(quantity - open_borrowstate_count_of_user, 0)


@bp.route("/checkin", methods=("POST",))
@authentication_required
@requires_permissions("manage_checkouts")
def checkin() -> Dict[str, Any]:
    """API endpoint for checkin of borrowed items."""
    checkin_request = CheckinRequestSchema().load(request.json)
    now = _utcnow()
    returning_user = User.query.get(checkin_request["user_id"])
    returned_items = [
        BorrowableItem.query.get(elem["id"]) for elem in checkin_request["item_ids"]
    ]
    borrowstates = []
    for item, elem in zip(returned_items, checkin_request["item_ids"]):
        qty = qty_before = elem["count"]
        for borrow_state in try_identify_borrowstates(returning_user, item, qty_before):
            #if borrow_state.borrowing_user == returning_user:
            if qty >= borrow_state.quantity:
                qty -= borrow_state.quantity
                borrow_state.returned_at = now
                borrowstates.append(borrow_state)
            else:
                borrow_state.quantity -= qty
                qty = 0
            if qty == 0:
                break
        else:
            item.unmatched_returns += qty
        item.quantity_in_stock += qty_before# - qty
    db.session.add(
        LogEntry(
            action="checkin",
            timestamp=now,
            subject=returning_user,
            items=returned_items,
        )
    )
    for transfer_request in TransferRequest.query.filter(
        TransferRequest.borrowstate_id.in_(bs.id for bs in borrowstates)
    ).all():
        db.session.delete(transfer_request)
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


def any_item_already_borrowed(items: Iterable[BorrowableItem], quantities: Iterable[int]) -> Sequence[Tuple[BorrowableItem, int]]:
    """Check if any item in item_ids already has an open borrowstate."""
    return [(item, count) for item, count in zip(items, quantities) if item.quantity_in_stock < count]
