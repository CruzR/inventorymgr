"""
Utility functions for access control.
"""

import functools
from typing import Any, Callable, Dict

from flask import session

from .api import APIError


PERMISSIONS = (
    'create_users',
    'view_users',
    'update_users',
    'edit_qualifications',
)

def can_set_permissions(user_dict: Dict[str, Any]) -> bool:
    """
    Check if current session's user can set permissions in user_dict.

    A user can set permissions if they are a subset of their own permissions.
    """
    return all(session['user'][k] or not user_dict[k] for k in PERMISSIONS)


def can_set_qualifications() -> bool:
    """Check if the current session's user can set qualifications."""
    return bool(session['user']['edit_qualifications'])


def requires_permissions(*permissions: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Wrap a view and check for permissions, raising APIError if user does not have them."""
    def outer(to_be_wrapped: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(to_be_wrapped)
        def inner(*args: Any, **kwargs: Any) -> Any:
            if not all(session['user'].get(p, False) for p in permissions):
                raise APIError(
                    'Insufficient permissions',
                    reason='insufficient_permissions',
                    status_code=403
                )
            return to_be_wrapped(*args, **kwargs)
        return inner
    return outer
