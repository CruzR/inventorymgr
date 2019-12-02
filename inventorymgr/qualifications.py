"""
Flask views for qualifications.

Qualifications are string tags that can be attached to a user to indicate they
hold some kind of qualification or skill, e.g. a driver's license.
"""

from typing import Any, Dict, cast

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError # type: ignore

from .accesscontrol import requires_permissions
from .api import APIError, QualificationSchema
from .auth import authentication_required
from .db import db
from .db.models import Qualification


bp = Blueprint('qualifications', __name__, url_prefix='/api/v1/qualifications')


@bp.route('', methods=('GET',))
@authentication_required
def list_qualifications() -> Dict[str, Any]:
    """API endpoint that returns a list of all qualifications."""
    qualifications_schema = QualificationSchema(many=True)
    qualifications = Qualification.query.all()
    return cast(Dict[str, Any], jsonify(qualifications_schema.dump(qualifications)))


@bp.route('', methods=('POST',))
@authentication_required
@requires_permissions('edit_qualifications')
def create_qualification() -> Dict[str, Any]:
    """API endpoint that creates a new qualification."""
    qualification_schema = QualificationSchema()
    qualification = qualification_schema.load(request.json, partial=('id',))

    if 'id' in qualification:
        raise APIError("Id specified", reason='id_specified', status_code=400)

    qualification_obj = Qualification(**qualification)

    try:
        db.session.add(qualification_obj)
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise APIError("Qualification exists", reason='object_exists', status_code=400) from exc

    return cast(Dict[str, Any], qualification_schema.dump(qualification_obj))


@bp.route('/<int:qual_id>', methods=('PUT',))
@authentication_required
@requires_permissions('edit_qualifications')
def update_qualification(qual_id: int) -> Dict[str, Any]:
    """API endpoint that updates an existing qualification."""
    qualification_schema = QualificationSchema()
    qualification = qualification_schema.load(request.json)
    if qualification['id'] != qual_id:
        raise APIError("Incorrect id", reason='incorrect_id', status_code=400)

    if Qualification.query.filter_by(id=qual_id).count() < 1:
        raise APIError("Qualification does not exist", reason='no_such_object', status_code=400)

    qualification_obj = Qualification.query.get(qual_id)
    qualification_obj.name = qualification['name']
    db.session.commit()

    return cast(Dict[str, Any], qualification)


@bp.route('/<int:qual_id>', methods=('DELETE',))
@authentication_required
@requires_permissions('edit_qualifications')
def delete_qualification(qual_id: int) -> Dict[str, bool]:
    """API endpoint that deletes a qualification."""
    qualification_schema = QualificationSchema()
    qualification = qualification_schema.load(request.json)
    if qualification['id'] != qual_id:
        raise APIError("Incorrect id", reason='incorrect_id', status_code=400)

    if Qualification.query.filter_by(id=qual_id).count() < 1:
        raise APIError("Qualification does not exist", reason='no_such_object', status_code=400)

    db.session.delete(Qualification.query.get(qual_id))
    db.session.commit()

    return {'success': True}
