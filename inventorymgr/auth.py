"""
Authentication views.

login()
    Flask view to log a user in.
"""

import functools
from typing import Any, Callable, cast, Dict

from flask import Blueprint, make_response, request, session
from werkzeug.security import check_password_hash as _check_password_hash

from inventorymgr import api
from inventorymgr.api import APIError
from inventorymgr.db.models import User


bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

_CHECK_HASH_ANYWAY = "pbkdf2:sha256:150000$tRQtwnYW$80442246fe5dbd649c8a90cd0209f7a3751e8a0ec1327f88f6b331f929642050"  # pylint: disable=line-too-long

check_password_hash: Callable[[str, str], bool] = cast(
    Callable[[str, str], bool], _check_password_hash
)


@bp.route("/login", methods=("POST",))
def login() -> Any:
    """Flask view for logging a user in."""
    user_obj = api.LoginRequest.parse_obj(request.json)
    username = user_obj.username
    password = user_obj.password

    if is_password_correct(username, password):
        user = fetch_user(username)
        session["user_id"] = user["id"]
        response = make_response(user)
        response.set_cookie("is_authenticated", "1")
        return response

    raise APIError(reason="invalid_user_or_password", status_code=403)


@bp.route("/logout", methods=("POST",))
def logout() -> Any:
    """Flask view to log a user out."""
    if "user_id" in session:
        del session["user_id"]
    response = make_response({"success": True})
    response.set_cookie("is_authenticated", max_age=0, expires=0)
    return response


def is_password_correct(username: str, password: str) -> bool:
    """Checks whether password is valid for user, tries to avoid timing attacks."""
    user = User.query.filter_by(username=username).first()
    if user is None:
        # We need to prevent timing-based side-channel attacks
        # that could be exploited for user enumeration
        password_hash = _CHECK_HASH_ANYWAY
    else:
        password_hash = user.password

    return check_password_hash(password_hash, password) and user is not None


def fetch_user(username: str) -> Dict[str, Any]:
    """Look up a user as a dictionary from the DB."""
    user = User.query.filter_by(username=username).first()
    return api.User.from_orm(user).dict()


def authentication_required(to_be_wrapped: Callable[..., Any]) -> Callable[..., Any]:
    """Wraps a view with a check for whether the user is authenticated."""

    @functools.wraps(to_be_wrapped)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        user_id = session.get("user_id")
        if user_id is None or User.query.get(user_id) is None:
            if "user_id" in session:
                del session["user_id"]
            response = make_response({"reason": "authentication_required"}, 403)
            response.set_cookie("is_authenticated", max_age=0, expires=0)
            return response
        return to_be_wrapped(*args, **kwargs)

    return wrapper
