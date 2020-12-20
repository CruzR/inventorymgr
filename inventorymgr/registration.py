"""Flask views for registration."""


import datetime
import secrets
from typing import Any, Dict, Tuple

import click
from flask import Blueprint, Response, make_response, request
from flask.cli import with_appcontext
from sqlalchemy.exc import IntegrityError  # type: ignore
from werkzeug.security import generate_password_hash

from inventorymgr import api
from inventorymgr.accesscontrol import requires_permissions
from inventorymgr.auth import authentication_required
from inventorymgr.db import db
from inventorymgr.db.models import RegistrationToken, User


bp = Blueprint("registration", __name__, url_prefix="/api/v1/registration")


@bp.route("/<token>", methods=("POST",))
def handle_registration_request(token: str) -> Tuple[Dict[str, Any], int]:
    """Flask view that handles submits of the registration form."""
    missing_fields = []
    for field in ("username", "password", "repeat_password"):
        if not request.json.get(field):
            missing_fields.append(field)
    if missing_fields:
        return {"reason": "missing_fields", "missing": missing_fields}, 400

    username = request.json["username"]
    password = request.json["password"]
    repeat_password = request.json["repeat_password"]

    if password != repeat_password:
        return {"reason": "password_mismatch"}, 400

    token_obj = RegistrationToken.query.filter_by(token=token).first()
    if token_obj is None:
        return {"reason": "invalid_token"}, 400

    if token_obj.expires < _utcnow():
        db.session.delete(token_obj)
        db.session.commit()
        return {"reason": "expired_token"}, 400

    db.session.delete(token_obj)
    db.session.commit()

    try:
        db.session.add(
            User(username=username, password=generate_password_hash(password))
        )
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

    return {"success": True}, 200


@bp.route("/tokens", methods=("GET",))
@authentication_required
@requires_permissions("create_users")
def get_tokens() -> Response:
    """Fetch a list of current registration tokens."""
    tokens = list(RegistrationToken.query.all())
    response = make_response(api.RegistrationTokenCollection(tokens=tokens).json(), 200)
    response.headers["Content-Type"] = "application/json; encoding=utf-8"
    return response


@bp.route("/tokens", methods=("POST",))
@authentication_required
@requires_permissions("create_users")
def create_token() -> Tuple[Dict[str, Any], int]:
    """Create a new registration token."""
    token = generate_registration_token()
    return api.RegistrationToken.from_orm(token).dict(), 200


@bp.route("/tokens/<int:token_id>", methods=("DELETE",))
@authentication_required
@requires_permissions("create_users")
def delete_token(token_id: int) -> Tuple[Dict[str, Any], int]:
    """Delete a registration token."""
    token = RegistrationToken.query.get(token_id)
    if token is not None:
        db.session.delete(token)
        db.session.commit()
    return {"success": True}, 200


@click.command("generate-registration-token")
@with_appcontext
def generate_registration_token_command() -> None:
    """CLI command to generate a registration token and print it."""
    token = generate_registration_token()
    click.echo(token.token)


def generate_registration_token() -> RegistrationToken:
    """Generate a new secure registration token and persist it."""
    for _ in range(3):
        token = secrets.token_hex()
        token_obj = RegistrationToken(
            token=token, expires=_utcnow() + datetime.timedelta(days=7)
        )
        try:
            db.session.add(token_obj)
            db.session.commit()
            return token_obj
        except IntegrityError:
            db.session.rollback()
    raise RuntimeError("Failed to generate a unique token in 3 tries.")


def _utcnow() -> datetime.datetime:
    """Allow mocking datetime.datetime.utcnow()."""
    return datetime.datetime.utcnow()
