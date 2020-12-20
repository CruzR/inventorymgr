"""API endpoints for dealing with borrowable items."""


from typing import Any, Dict, Tuple
from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError  # type: ignore

from inventorymgr import api
from inventorymgr.accesscontrol import requires_permissions
from inventorymgr.api import APIError
from inventorymgr.auth import authentication_required
from inventorymgr.db import db
from inventorymgr.db.models import BorrowableItem, Qualification


bp = Blueprint("items", __name__, url_prefix="/api/v1/items")


@bp.route("", methods=("POST",))
@authentication_required
@requires_permissions("create_items")
def create_item() -> Tuple[Dict[str, Any], int]:
    """JSON endpoint for creating borrowable items."""
    received_item = api.NewItem.parse_obj(request.json)
    try:
        qual_ids = [q.id for q in received_item.required_qualifications]
        qualifications = [Qualification.query.get(q_id) for q_id in qual_ids]
        if any(q is None for q in qualifications):
            raise APIError(reason="unknown_qualification", status_code=400)
        item = BorrowableItem(
            name=received_item.name, required_qualifications=qualifications
        )
        db.session.add(item)
        db.session.commit()
        return api.BorrowableItem.from_orm(item).dict(), 200
    except IntegrityError as exc:
        raise APIError(reason="item_exists", status_code=400) from exc


@bp.route("", methods=("GET",))
@authentication_required
def list_items() -> Dict[str, Any]:
    """JSON endpoint for getting all borrowable items."""
    items = list(BorrowableItem.query.all())
    return api.BorrowableItemCollection(items=items).dict()


@bp.route("/<int:item_id>", methods=("PUT",))
@authentication_required
@requires_permissions("create_items")
def update_item(item_id: int) -> Dict[str, Any]:
    """JSON endpoint for updating borrowable item."""
    received_item = api.UpdatedItem.parse_obj(request.json)

    if received_item.id != item_id:
        raise APIError(reason="id_mismatch", status_code=400)

    item = BorrowableItem.query.get(item_id)
    if item is None:
        raise APIError(reason="nonexistent_item", status_code=400)

    qual_ids = [q.id for q in received_item.required_qualifications]
    qualifications = [Qualification.query.get(q_id) for q_id in qual_ids]
    if any(q is None for q in qualifications):
        raise APIError(reason="unknown_qualification", status_code=400)

    try:
        item.name = received_item.name
        item.required_qualifications = qualifications
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise APIError(reason="item_exists", status_code=400) from exc

    return api.BorrowableItem.from_orm(item).dict()


@bp.route("/<int:item_id>", methods=("DELETE",))
@authentication_required
@requires_permissions("create_items")
def delete_item(item_id: int) -> Dict[str, Any]:
    """API endpoint for deleting borrowable items."""
    item = BorrowableItem.query.get(item_id)
    if item is not None:
        db.session.delete(item)
        db.session.commit()
    return {"success": True}


@bp.route("/<int:item_id>", methods=("GET",))
@authentication_required
def get_item(item_id: int) -> Any:
    """API endpoint for getting a single borrowable item."""
    item = BorrowableItem.query.get(item_id)
    if item is None:
        raise APIError(reason="nonexistent_item", status_code=400)
    return api.BorrowableItem.from_orm(item).dict()
