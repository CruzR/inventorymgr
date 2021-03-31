"""Business logic regarding users."""


from typing import cast

from sqlalchemy.exc import IntegrityError  # type: ignore
from werkzeug.security import generate_password_hash

from inventorymgr import api
from inventorymgr.accesscontrol import (
    PERMISSIONS,
    can_set_permissions,
    can_set_qualifications,
)
from inventorymgr.db import db
from inventorymgr.db.models import Qualification, User

__all__ = ["create_user", "read_user", "update_user", "delete_user"]


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


def read_user(user_id: int) -> User:
    """Read a specified user from the DB."""
    user = User.query.get(user_id)
    if user is None:
        raise api.APIError(reason="no_such_user", status_code=400)
    return cast(User, user)


def update_user(user_id: int, user_obj: api.UpdatedUser) -> User:
    """Update an existing user."""
    if user_obj.id != user_id:
        raise api.APIError(reason="incorrect_id", status_code=400)

    user = User.query.get(user_id)
    if user is None:
        raise api.APIError(reason="no_such_user", status_code=400)

    try:
        update_user_qualifications(user, user_obj)
        update_user_permissions(user, user_obj)
        update_user_username(user, user_obj)
        update_user_password(user, user_obj)
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise api.APIError(reason="user_exists", status_code=400) from exc

    return cast(User, user)


def delete_user(user_id: int) -> None:
    """Delete a user if they exist."""
    user = User.query.get(user_id)
    if user is not None:
        db.session.delete(User.query.get(user_id))
        db.session.commit()


def update_user_qualifications(user: User, user_obj: api.UpdatedUser) -> None:
    """Update user qualifications."""
    current_qualifications = {q.id for q in user.qualifications}
    new_qualifications = {q.id for q in user_obj.qualifications}

    if current_qualifications != new_qualifications:
        if not can_set_qualifications():
            raise insufficient_permissions()
        qualifications = [Qualification.query.get(q_id) for q_id in new_qualifications]
        if any(q is None for q in qualifications):
            raise api.APIError(reason="unknown_qualification", status_code=400)
        user.qualifications = qualifications


def update_user_permissions(user: User, user_obj: api.UpdatedUser) -> None:
    """Update user permissions."""
    if wants_to_update_permissions(user, user_obj):
        if not can_set_permissions(user_obj):
            raise api.APIError(reason="permissions_not_subset", status_code=403)
        for perm in PERMISSIONS:
            setattr(user, perm, getattr(user_obj, perm))


def update_user_username(user: User, user_obj: api.UpdatedUser) -> None:
    """Update username."""
    user.username = user_obj.username


def update_user_password(user: User, user_obj: api.UpdatedUser) -> None:
    """Update user password."""
    if user_obj.password is not None:
        user.password = generate_password_hash(user_obj.password)


def insufficient_permissions() -> api.APIError:
    """Return an API error for insufficient permissions."""
    return api.APIError(reason="insufficient_permissions", status_code=403)


def wants_to_update_permissions(user: User, user_obj: api.UpdatedUser) -> bool:
    """Check if permissions need updating."""
    return any(getattr(user_obj, p) != getattr(user, p) for p in PERMISSIONS)
