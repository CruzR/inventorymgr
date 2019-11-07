"""
Utility functions for access control.
"""

import functools
from typing import Any, Callable

from flask import session

from .api import APIError


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
