"""API endpoints for dealing with borrowable items."""


from typing import Any, Dict, Tuple, cast
from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError # type: ignore

from inventorymgr.accesscontrol import requires_permissions
from inventorymgr.api import APIError
from inventorymgr.api.models import BorrowableItemSchema
from inventorymgr.auth import authentication_required
from inventorymgr.db import db
from inventorymgr.db.models import BorrowableItem


bp = Blueprint('items', __name__, url_prefix='/api/v1/items')


@bp.route('', methods=('POST',))
@authentication_required
@requires_permissions('create_items')
def create_item() -> Tuple[Dict[str, Any], int]:
    """JSON endpoint for creating borrowable items."""
    received_item = BorrowableItemSchema(only=('name',)).load(request.json)
    try:
        item = BorrowableItem(name=received_item['name'])
        db.session.add(item)
        db.session.commit()
        return BorrowableItemSchema().dump(item), 200
    except IntegrityError as exc:
        raise APIError(
            'Item already exists',
            reason='item_exists',
            status_code=400) from exc


@bp.route('', methods=('GET',))
@authentication_required
def list_items() -> Dict[str, Any]:
    """JSON endpoint for getting all borrowable items."""
    items = BorrowableItemSchema(many=True).dump(BorrowableItem.query.all())
    return {'items': items}


@bp.route('/<int:item_id>', methods=('PUT',))
@authentication_required
@requires_permissions('create_items')
def update_item(item_id: int) -> Dict[str, Any]:
    """JSON endpoint for updating borrowable item."""
    schema = BorrowableItemSchema()
    received_item = schema.load(request.json)

    if received_item['id'] != item_id:
        raise APIError('Item ids do not match', reason='id_mismatch', status_code=400)

    item = BorrowableItem.query.get(item_id)
    if item is None:
        raise APIError('Item does not exist', reason='nonexistent_item', status_code=400)

    item.name = received_item['name']
    db.session.commit()

    return cast(Dict[str, Any], schema.dump(item))
