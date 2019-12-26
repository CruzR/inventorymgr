"""Flask views for registration."""


import datetime
import secrets
from typing import Any, Dict, Tuple

import click
from flask import Blueprint, request
from flask.cli import with_appcontext
from sqlalchemy.exc import IntegrityError # type: ignore
from werkzeug.security import generate_password_hash

from .db import db
from .db.models import RegistrationToken, User


bp = Blueprint('registration', __name__, url_prefix='/api/v1/registration')


@bp.route('/<token>', methods=('POST',))
def handle_registration_request(token: str) -> Tuple[Dict[str, Any], int]:
    """Flask view that handles submits of the registration form."""
    missing_fields = []
    for field in ('username', 'password', 'repeat_password'):
        if not request.json.get(field):
            missing_fields.append(field)
    if missing_fields:
        return {'reason': 'missing_fields', 'missing': missing_fields}, 400

    username = request.json['username']
    password = request.json['password']
    repeat_password = request.json['repeat_password']

    if password != repeat_password:
        return {'reason': 'password_mismatch'}, 400

    token_obj = RegistrationToken.query.filter_by(token=token).first()
    if token_obj is None:
        return {'reason': 'invalid_token'}, 400

    if token_obj.expires < datetime.datetime.now():
        db.session.delete(token_obj)
        db.session.commit()
        return {'reason': 'expired_token'}, 400

    db.session.delete(token_obj)
    db.session.commit()

    try:
        db.session.add(
            User(username=username, password=generate_password_hash(password)))
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

    return {'success': True}, 200


@click.command('generate-registration-token')
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
            token=token,
            expires=datetime.datetime.now() + datetime.timedelta(days=7)
        )
        try:
            db.session.add(token_obj)
            db.session.commit()
            return token_obj
        except IntegrityError:
            db.session.rollback()
    raise RuntimeError('Failed to generate a unique token in 3 tries.')
