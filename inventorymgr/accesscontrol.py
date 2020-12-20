"""
Utility functions for access control.
"""

import functools
from typing import Any, Callable, Union, cast

from flask import session

from inventorymgr import api
from inventorymgr.api import APIError
from inventorymgr.db.models import User


PERMISSIONS = (
    "create_users",
    "view_users",
    "update_users",
    "edit_qualifications",
    "create_items",
    "manage_checkouts",
)


def can_set_permissions(
    user_obj: Union[api.User, api.NewUser, api.UpdatedUser]
) -> bool:
    """
    Check if current session's user can set permissions in user_dict.

    A user can set permissions if they are a subset of their own permissions.
    """
    user = get_session_user()
    return all(getattr(user, k) or not getattr(user_obj, k) for k in PERMISSIONS)


def can_set_qualifications() -> bool:
    """Check if the current session's user can set qualifications."""
    return cast(bool, get_session_user().edit_qualifications)


def requires_permissions(
    *permissions: str,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Wrap a view and check for permissions, raising APIError if user does not have them."""

    def outer(to_be_wrapped: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(to_be_wrapped)
        def inner(*args: Any, **kwargs: Any) -> Any:
            user = get_session_user()
            if not all(getattr(user, p, False) for p in permissions):
                raise APIError(reason="insufficient_permissions", status_code=403)
            return to_be_wrapped(*args, **kwargs)

        return inner

    return outer


def get_session_user() -> User:
    """Get the current session user."""
    return cast(User, User.query.get(session["user_id"]))
