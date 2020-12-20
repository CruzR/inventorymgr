"""
Flask views for qualifications.

Qualifications are string tags that can be attached to a user to indicate they
hold some kind of qualification or skill, e.g. a driver's license.
"""

from typing import Any, Dict

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError  # type: ignore

from inventorymgr import api
from inventorymgr.accesscontrol import requires_permissions
from inventorymgr.api import APIError
from inventorymgr.auth import authentication_required
from inventorymgr.db import db
from inventorymgr.db.models import Qualification


bp = Blueprint("qualifications", __name__, url_prefix="/api/v1/qualifications")


@bp.route("", methods=("GET",))
@authentication_required
def list_qualifications() -> Dict[str, Any]:
    """API endpoint that returns a list of all qualifications."""
    qualifications = list(Qualification.query.all())
    return api.QualificationCollection(qualifications=qualifications).dict()


@bp.route("", methods=("POST",))
@authentication_required
@requires_permissions("edit_qualifications")
def create_qualification() -> Dict[str, Any]:
    """API endpoint that creates a new qualification."""
    qualification_obj = api.NewQualification.parse_obj(request.json)

    if hasattr(qualification_obj, "id"):
        raise APIError(reason="id_specified", status_code=400)

    qualification = Qualification(**qualification_obj.dict())

    try:
        db.session.add(qualification)
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise APIError(reason="object_exists", status_code=400) from exc

    return api.Qualification.from_orm(qualification).dict()


@bp.route("/<int:qual_id>", methods=("PUT",))
@authentication_required
@requires_permissions("edit_qualifications")
def update_qualification(qual_id: int) -> Dict[str, Any]:
    """API endpoint that updates an existing qualification."""
    qualification_obj = api.Qualification.parse_obj(request.json)
    if qualification_obj.id != qual_id:
        raise APIError(reason="incorrect_id", status_code=400)

    if Qualification.query.filter_by(id=qual_id).count() < 1:
        raise APIError(reason="no_such_object", status_code=400)

    qualification = Qualification.query.get(qual_id)

    try:
        qualification.name = qualification_obj.name
        db.session.commit()
    except IntegrityError as exc:
        raise APIError(reason="qualification_exists", status_code=400) from exc

    return api.Qualification.from_orm(qualification).dict()


@bp.route("/<int:qual_id>", methods=("DELETE",))
@authentication_required
@requires_permissions("edit_qualifications")
def delete_qualification(qual_id: int) -> Dict[str, bool]:
    """API endpoint that deletes a qualification."""
    qualification_obj = api.Qualification.parse_obj(request.json)
    if qualification_obj.id != qual_id:
        raise APIError(reason="incorrect_id", status_code=400)

    if Qualification.query.filter_by(id=qual_id).count() < 1:
        raise APIError(reason="no_such_object", status_code=400)

    db.session.delete(Qualification.query.get(qual_id))
    db.session.commit()

    return {"success": True}


@bp.route("/<int:qual_id>", methods=("GET",))
@authentication_required
def get_qualification(qual_id: int) -> Any:
    """API endpoint to fetch a single qualification."""
    qualification = Qualification.query.get(qual_id)
    if qualification is None:
        raise APIError(reason="no_such_object", status_code=400)
    return api.Qualification.from_orm(qualification).dict()
