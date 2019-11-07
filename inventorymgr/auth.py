"""
Authentication views.

login()
    Flask view to log a user in.
"""

from typing import Callable, Dict, cast

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

    if check_password_hash(password_hash, password) and password_row is not None:
        session['username'] = username
        return {'success': True}

    raise APIError(
        'Invalid username or password',
        reason='invalid_user_or_password',
        status_code=403
    )
