"""
User management views.

new_user()
    Flask view to create a new user using POST.

update_user()
    Flask view to update a user using PUT.

list_users()
    Flask view to get a list of users using GET.
"""

import sqlite3
from typing import Dict, List

from flask import Blueprint, request
from werkzeug.security import generate_password_hash

from .api import APIError
from .db import get_db


# This is the conventional name for Blueprint objects, disable the warning.
bp = Blueprint('users', __name__, url_prefix='/users') # pylint: disable=invalid-name


@bp.route('/', methods=('POST',))
def new_user() -> Dict[str, bool]:
    """Flask view to create a new user using POST."""
    username = request.json['username']
    password = request.json['password']
    db = get_db()

    try:
        db.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)',
            (username, generate_password_hash(password))
        )
        db.commit()
    except sqlite3.IntegrityError as exc:
        raise APIError('Username already taken', reason='user_exists', status_code=400) from exc

    return {'success': True}


@bp.route('/', methods=('PUT',))
def update_user() -> Dict[str, bool]:
    """Flask view to update a user using PUT."""
    username = request.json['username']
    password = request.json['password']
    db = get_db()

    cursor = db.execute(
        'UPDATE users SET password = ? WHERE username = ?',
        (generate_password_hash(password), username)
    )

    if cursor.rowcount < 1:
        db.rollback()
        raise APIError('No such user', reason='no_such_user', status_code=400)

    db.commit()

    return {'success': True}


@bp.route('/', methods=('GET',))
def list_users() -> Dict[str, List[str]]:
    """Flask view to get a list of users using GET."""
    db = get_db()
    users = [username for username, in db.execute('SELECT username FROM users;')]
    return {'users': users}
