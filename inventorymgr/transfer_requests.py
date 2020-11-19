"""API endpoints for transfer requests."""

import datetime
from typing import Any, Dict

from flask import Blueprint, request, session

from inventorymgr.api import APIError
from inventorymgr.api.models import TransferRequestCollection, NewTransferRequest
from inventorymgr.auth import authentication_required
from inventorymgr.db import db
from inventorymgr.db.models import BorrowState, LogEntry, TransferRequest, User


bp = Blueprint("transfer_requests", __name__, url_prefix="/api/v1/transferrequests")


@bp.route("", methods=("GET",))
@authentication_required
def get_transfer_requests() -> Dict[str, Any]:
    """Returns a list of transfer requests for the current user."""
    return TransferRequestCollection(
        transferrequests=list(
            TransferRequest.query.filter_by(target_user_id=session["user_id"])
        )
    ).dict()


@bp.route("", methods=("POST",))
@authentication_required
def create_transfer_request() -> Dict[str, bool]:
    """API endpoint for creating transfer requests."""
    transfer_request_data = NewTransferRequest.parse_obj(request.json)
    borrowstate = BorrowState.query.get(transfer_request_data.borrowstate_id)
    issuing_user = User.query.get(session["user_id"])
    if borrowstate is None:
        raise APIError(reason="unknown_borrowstate", status_code=400)
    if borrowstate.borrowing_user_id != issuing_user.id:
        raise APIError(reason="insufficient_permissions", status_code=403)
    if borrowstate.returned_at is not None:
        raise APIError(reason="item_not_borrowed", status_code=400)
    target_user = User.query.get(transfer_request_data.target_user_id)
    item = borrowstate.borrowed_item
    if not set(item.required_qualifications) <= set(target_user.qualifications):
        raise APIError(reason="missing_qualifications", status_code=403)
    transfer_request = TransferRequest(
        target_user=target_user, issuing_user=issuing_user, borrowstate=borrowstate
    )
    db.session.add(transfer_request)
    db.session.commit()
    return {"success": True}


@bp.route("/<int:request_id>", methods=("DELETE",))
@authentication_required
def accept_or_decline_transfer_request(request_id: int) -> Dict[str, bool]:
    """API endpoint to accept or decline a transfer request."""
    user = User.query.get(session["user_id"])
    transfer_request = TransferRequest.query.get(request_id)
    if transfer_request is None:
        raise APIError(reason="unknown_transfer_request", status_code=404)
    if user.id != transfer_request.target_user_id:
        raise APIError(reason="insufficient_permissions", status_code=403)
    if (
        transfer_request.borrowstate.borrowing_user_id
        != transfer_request.issuing_user_id
    ):
        db.session.delete(transfer_request)
        db.session.commit()
        raise APIError(reason="insufficient_permissions", status_code=403)
    if request.json["action"] == "accept":
        item = transfer_request.borrowstate.borrowed_item
        if not set(item.required_qualifications) <= set(user.qualifications):
            raise APIError(reason="missing_qualifications", status_code=403)
        db.session.add(
            LogEntry(
                action="transfer",
                timestamp=_utcnow(),
                subject=transfer_request.borrowstate.borrowing_user,
                secondary=user,
                items=[transfer_request.borrowstate.borrowed_item],
            )
        )
        transfer_request.borrowstate.borrowing_user = user
    elif request.json["action"] != "decline":
        raise APIError(reason="unknown_transfer_request_action", status_code=400)
    db.session.delete(transfer_request)
    db.session.commit()
    return {"success": True}


def _utcnow() -> datetime.datetime:
    return datetime.datetime.utcnow()
