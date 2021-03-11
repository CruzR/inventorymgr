"""Business logic regarding users."""


from werkzeug.security import generate_password_hash

from inventorymgr import api
from inventorymgr.accesscontrol import (
    PERMISSIONS,
    can_set_permissions,
    can_set_qualifications,
)
from inventorymgr.db import db
from inventorymgr.db.models import Qualification, User

__all__ = ["create_user"]


def create_user(user_obj: api.NewUser) -> User:
    """Create a new user."""
    username = user_obj.username
    password = user_obj.password

    if user_obj.qualifications and not can_set_qualifications():
        raise insufficient_permissions()

    if not can_set_permissions(user_obj):
        raise api.APIError(reason="permissions_not_subset", status_code=403)

    qualifications = [Qualification.query.get(q.id) for q in user_obj.qualifications]

    user = User(
        username=username,
        password=generate_password_hash(password),
        qualifications=qualifications,
        **{k: getattr(user_obj, k) for k in PERMISSIONS},
    )

    db.session.add(user)
    db.session.commit()
    return user


def insufficient_permissions() -> api.APIError:
    """Return an API error for insufficient permissions."""
    return api.APIError(reason="insufficient_permissions", status_code=403)
