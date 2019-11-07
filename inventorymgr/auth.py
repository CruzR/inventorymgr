"""
Authentication views.

login()
    Flask view to log a user in.
"""

import functools
from typing import Any, Callable, cast, Dict

from flask import Blueprint, request, session
from werkzeug.security import check_password_hash as _check_password_hash

from .api import APIError
from .db import get_db


# This is the conventional name for Blueprint objects, disable the warning.
bp = Blueprint('auth', __name__, url_prefix='/auth') # pylint: disable=invalid-name

_CHECK_HASH_ANYWAY = 'pbkdf2:sha256:150000$tRQtwnYW$80442246fe5dbd649c8a90cd0209f7a3751e8a0ec1327f88f6b331f929642050' # pylint: disable=line-too-long

check_password_hash: Callable[[str, str], bool] = cast(Callable[[str, str], bool], _check_password_hash) # pylint: disable=line-too-long


@bp.route('/login', methods=('POST',))
def login() -> Dict[str, bool]:
    """Flask view for logging a user in."""
    username = request.json['username']
    password = request.json['password']

    if is_password_correct(username, password):
        session['user'] = fetch_user(username)
        return {'success': True}

    raise APIError(
        'Invalid username or password',
        reason='invalid_user_or_password',
        status_code=403
    )


def is_password_correct(username: str, password: str) -> bool:
    """Checks whether password is valid for user, tries to avoid timing attacks."""
    db = get_db()
    password_row = db.execute(
        'SELECT password FROM users WHERE username = ?',
        (username,)
    ).fetchone()

    if password_row is None:
        # We need to prevent timing-based side-channel attacks
        # that could be exploited for user enumeration
        password_hash = _CHECK_HASH_ANYWAY
    else:
        password_hash = password_row['password']

    return check_password_hash(password_hash, password) and password_row is not None


def fetch_user(username: str) -> Dict[str, Any]:
    """Look up a user as a dictionary from the DB."""
    user_row = get_db().execute(
        'SELECT * FROM users WHERE username = ?',
        (username,)
    ).fetchone()
    return dict(user_row)


def authentication_required(to_be_wrapped: Callable[..., Any]) -> Callable[..., Any]:
    """Wraps a view with a check for whether the user is authenticated."""
    @functools.wraps(to_be_wrapped)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if session.get('user') is None:
            raise APIError(
                'Authentication required',
                reason='authentication_required',
                status_code=403
            )
        return to_be_wrapped(*args, **kwargs)
    return wrapper
