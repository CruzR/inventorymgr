"""Flask views for registration."""


import datetime
import secrets
from typing import cast, Tuple, Union

import click
from flask import Blueprint, redirect, render_template, request, url_for
from flask.cli import with_appcontext
from sqlalchemy.exc import IntegrityError # type: ignore
from werkzeug.security import generate_password_hash
from werkzeug.wrappers import Response

from .db import db
from .db.models import RegistrationToken, User


bp = Blueprint('registration', __name__)


@bp.route('/register/<token>', methods=('GET',))
def register(token: str) -> str:
    """Flask view that returns a registration form."""
    # pylint: disable=unused-argument
    return render_template('registration/register.html')


@bp.route('/register/<token>', methods=('POST',))
def handle_registration_request(token: str) -> Union[Response, Tuple[str, int]]:
    """Flask view that handles submits of the registration form."""
    errors = []
    for field in ('username', 'password', 'repeat_password'):
        if not request.form.get(field):
            errors.append('Field "{}" is required'.format(field))
    if errors:
        return render_template('registration/register.html', errors=errors), 400

    username = request.form['username']
    password = request.form['password']
    repeat_password = request.form['repeat_password']

    if password != repeat_password:
        return render_template(
            'registration/register.html',
            errors=['Passwords do not match'],
            username=username
        ), 400

    token_obj = RegistrationToken.query.filter_by(token=token).first()
    if token_obj is None:
        return render_template(
            'registration/register.html',
            errors=['Invalid registration token'],
            username=username
        ), 400

    if token_obj.expires < datetime.datetime.now():
        db.session.delete(token_obj)
        db.session.commit()
        return render_template(
            'registration/register.html',
            errors=['Registration token has expired.'],
            username=username
        ), 400

    db.session.delete(token_obj)
    db.session.commit()

    try:
        db.session.add(
            User(username=username, password=generate_password_hash(password)))
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

    return redirect(url_for('registration.success_or_user_exists'))


@bp.route('/register/success')
def success_or_user_exists() -> str:
    """Flask view that is rendered when registration appeared successfull."""
    return render_template('registration/success_or_user_exists.html')


@click.command('generate-registration-token')
@with_appcontext
def generate_registration_token_command() -> None:
    """CLI command to generate a registration token and print it."""
    token = generate_registration_token()
    click.echo(registration_url(token))


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


def registration_url(token: RegistrationToken) -> str:
    """Build a registration URL from a registration token."""
    return cast(str, url_for('registration.register', token=token.token))
