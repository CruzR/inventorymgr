"""
User management views.

new_user()
    Flask view to create a new user using POST.

update_user()
    Flask view to update a user using PUT.

list_users()
    Flask view to get a list of users using GET.
"""

from typing import Dict, List

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError # type: ignore
from werkzeug.security import generate_password_hash

from .accesscontrol import requires_permissions
from .api import APIError
from .auth import authentication_required
from .db import db
from .db.models import User


bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/', methods=('POST',))
def new_user() -> Dict[str, bool]:
    """Flask view to create a new user using POST."""
    username = request.json['username']
    password = request.json['password']

    try:
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
    except IntegrityError as exc:
        raise APIError('Username already taken', reason='user_exists', status_code=400) from exc

    return {'success': True}


@bp.route('/', methods=('PUT',))
@authentication_required
@requires_permissions('view_users', 'update_user')
def update_user() -> Dict[str, bool]:
    """Flask view to update a user using PUT."""
    username = request.json['username']
    password = request.json['password']

    user = User.query.filter_by(username=username).first()
    if user is None:
        raise APIError('No such user', reason='no_such_user', status_code=400)

    user.password = generate_password_hash(password)
    db.session.add(user)
    db.session.commit()

    return {'success': True}


@bp.route('/', methods=('GET',))
@authentication_required
@requires_permissions('view_users')
def list_users() -> Dict[str, List[str]]:
    """Flask view to get a list of users using GET."""
    users = [user.username for user in User.query.all()]
    return {'users': users}
