"""
User management views.

new_user()
    Flask view to create a new user using POST.

update_user()
    Flask view to update a user using PUT.

list_users()
    Flask view to get a list of users using GET.
"""

from typing import Any, Dict, List, cast

import click
from flask import Blueprint, request, session
from flask.cli import with_appcontext
from sqlalchemy.exc import IntegrityError # type: ignore
from werkzeug.security import generate_password_hash

from .accesscontrol import (PERMISSIONS, can_set_permissions,
                            can_set_qualifications, requires_permissions)
from .api import APIError, UserSchema
from .auth import authentication_required
from .db import db
from .db.models import User, Qualification


bp = Blueprint('users', __name__, url_prefix='/api/v1/users')


@bp.route('', methods=('POST',))
@authentication_required
@requires_permissions('create_users')
def new_user() -> Dict[str, Any]:
    """Flask view to create a new user using POST."""
    user_schema = UserSchema()
    user_dict = user_schema.load(request.json, partial=('id',))
    username = user_dict['username']
    password = user_dict['password']

    if user_dict['qualifications'] and not can_set_qualifications():
        raise APIError(
            "Requires edit_qualifications",
            reason="insufficient_permissions",
            status_code=403
        )

    if not can_set_permissions(user_dict):
        raise APIError(
            "Cannot set permissions",
            reason="permissions_not_subset",
            status_code=403
        )

    qualifications = [
        Qualification.query.get(q['id']) for q in user_dict['qualifications']]

    try:
        user = User(
            username=username,
            password=generate_password_hash(password),
            qualifications=qualifications,
            **{k: user_dict[k] for k in PERMISSIONS},
        )

        db.session.add(user)
        db.session.commit()
        return cast(Dict[str, Any], user_schema.dump(user))

    except IntegrityError as exc:
        raise APIError('Username already taken', reason='user_exists', status_code=400) from exc


@bp.route('/<int:user_id>', methods=('PUT',))
@authentication_required
@requires_permissions('view_users', 'update_users')
def update_user(user_id: int) -> Dict[str, Any]:
    """Flask view to update a user using PUT."""
    user_schema = UserSchema()
    user_dict = user_schema.load(request.json, partial=('password',))

    if user_dict['id'] != user_id:
        raise APIError("Incorrect id", reason='incorrect_id', status_code=400)

    user = User.query.get(user_id)
    if user is None:
        raise APIError('No such user', reason='no_such_user', status_code=400)

    current_qualifications = {q.id for q in user.qualifications}
    new_qualifications = {q['id'] for q in user_dict['qualifications']}

    if current_qualifications != new_qualifications:
        if not can_set_qualifications():
            raise APIError(
                "Requires edit_qualifications",
                reason="insufficient_permissions",
                status_code=403
            )
        qualifications = [Qualification.query.get(q_id) for q_id in new_qualifications]
        user.qualifications = qualifications

    if any(user_dict[p] != getattr(user, p) for p in PERMISSIONS):
        if not can_set_permissions(user_dict):
            raise APIError(
                "Cannot set permissions",
                reason="permissions_not_subset",
                status_code=403
            )
        for perm in PERMISSIONS:
            setattr(user, perm, user_dict[perm])

    user.username = user_dict['username']
    if 'password' in user_dict:
        user.password = generate_password_hash(user_dict['password'])

    db.session.commit()

    return cast(Dict[str, Any], user_schema.dump(user))


@bp.route('/<int:user_id>', methods=('DELETE',))
@authentication_required
@requires_permissions('view_users', 'update_users')
def delete_user(user_id: int) -> str:
    """Flask view to delete a user with DELETE."""

    user = User.query.get(user_id)
    if user is not None:
        db.session.delete(User.query.get(user_id))
        db.session.commit()

    return str(user_id)


@bp.route('/me', methods=('GET',))
@authentication_required
def get_self() -> Any:
    """Flask view to get the current session's user as JSON."""
    self_id = session['user']['id']
    self_user = User.query.get(self_id)
    if self_user is None:
        raise APIError('No such user', reason='no_such_user', status_code=400)
    return UserSchema().dump(self_user)


@bp.route('', methods=('GET',))
@authentication_required
@requires_permissions('view_users')
def list_users() -> Dict[str, List[str]]:
    """Flask view to get a list of users using GET."""
    users = UserSchema(many=True).dump(User.query.all())
    return {'users': users}


@click.command('create-user')
@click.option('--username', prompt='Username')
@click.option('--password', prompt='Password', confirmation_prompt=True, hide_input=True)
@click.option('--create-users', prompt='Permission create_users [y/n]', type=bool)
@click.option('--view-users', prompt="Permission view_users [y/n]", type=bool)
@click.option('--update-users', prompt="Permission update_users [y/n]", type=bool)
@click.option('--edit-qualifications', prompt="Permission edit_qualifications [y/n]", type=bool)
@with_appcontext
def create_user_command(**args: Any) -> None:
    """CLI command to create a new user."""
    args['password'] = generate_password_hash(args['password'])
    db.session.add(User(**args))
    db.session.commit()
    click.echo('Created user {}'.format(args['username']))
