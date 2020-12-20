"""Package containing API datatype definitions."""

from typing import Dict, Tuple

from flask import Blueprint

from inventorymgr.api import models
from inventorymgr.api.error import APIError, handle_api_error, handle_validation_error
from inventorymgr.api.models import *

__all__ = [
    "APIError",
    "handle_api_error",
    "handle_validation_error",
    "bp",
    "Qualification",
    "QualificationCollection",
    "NewQualification",
    "LoginRequest",
    "User",
    "UserCollection",
    "UserInfo",
    "NewUser",
    "UpdatedUser",
    "RegistrationToken",
    "RegistrationTokenCollection",
    "BorrowableItem",
    "BorrowableItemCollection",
    "NewItem",
    "UpdatedItem",
    "BorrowState",
    "BorrowStateCollection",
    "CheckoutRequest",
    "CheckinRequest",
    "LogEntry",
    "LogEntryCollection",
    "NewTransferRequest",
    "TransferRequest",
    "TransferRequestCollection",
]


bp = Blueprint("api", __name__)


_ALL_METHODS = ("GET", "HEAD", "POST", "PUT", "PATCH", "DELETE")


@bp.route("/api/", methods=_ALL_METHODS, defaults={"path": ""})
@bp.route("/api/<path:path>", methods=_ALL_METHODS)
def unknown_resource(path: str) -> Tuple[Dict[str, str], int]:
    """Return 404 if no route is registered for a resource."""
    resource = f"/api/{path}"
    return {"reason": "unknown_resource", "resource": resource}, 404
