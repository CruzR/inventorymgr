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
from sqlalchemy.exc import IntegrityError  # type: ignore
from werkzeug.security import generate_password_hash

from .accesscontrol import (
    PERMISSIONS,
    can_set_permissions,
    can_set_qualifications,
    requires_permissions,
)
from .api import APIError, UserSchema
from .auth import authentication_required, logout
from .db import db
from .db.models import User, Qualification


bp = Blueprint("users", __name__, url_prefix="/api/v1/users")


@bp.route("", methods=("POST",))
@authentication_required
@requires_permissions("create_users")
def new_user() -> Dict[str, Any]:
    """Flask view to create a new user using POST."""
    user_schema = UserSchema()
    user_dict = user_schema.load(request.json, partial=("id",))
    username = user_dict["username"]
    password = user_dict["password"]

    if user_dict["qualifications"] and not can_set_qualifications():
        raise insufficient_permissions()

    if not can_set_permissions(user_dict):
        raise APIError(reason="permissions_not_subset", status_code=403)

    qualifications = [
        Qualification.query.get(q["id"]) for q in user_dict["qualifications"]
    ]

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
        raise APIError(reason="user_exists", status_code=400) from exc


@bp.route("/<int:user_id>", methods=("PUT",))
@authentication_required
@requires_permissions("view_users", "update_users")
def update_user(user_id: int) -> Dict[str, Any]:
    """Flask view to update a user using PUT."""
    user_schema = UserSchema()
    user_dict = user_schema.load(request.json, partial=("password",))

    if user_dict["id"] != user_id:
        raise APIError(reason="incorrect_id", status_code=400)

    user = User.query.get(user_id)
    if user is None:
        raise APIError(reason="no_such_user", status_code=400)

    try:
        update_user_qualifications(user, user_dict)
        update_user_permissions(user, user_dict)
        update_user_username(user, user_dict)
        update_user_password(user, user_dict)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise APIError(reason="user_exists", status_code=400)

    return cast(Dict[str, Any], user_schema.dump(user))


def update_user_qualifications(user: User, user_dict: Dict[str, Any]) -> None:
    """Update user qualifications."""
    current_qualifications = {q.id for q in user.qualifications}
    new_qualifications = {q["id"] for q in user_dict["qualifications"]}

    if current_qualifications != new_qualifications:
        if not can_set_qualifications():
            raise insufficient_permissions()
        qualifications = [Qualification.query.get(q_id) for q_id in new_qualifications]
        if any(q is None for q in qualifications):
            raise APIError(reason="unknown_qualification", status_code=400)
        user.qualifications = qualifications


def update_user_permissions(user: User, user_dict: Dict[str, Any]) -> None:
    """Update user permissions."""
    if wants_to_update_permissions(user, user_dict):
        if not can_set_permissions(user_dict):
            raise APIError(reason="permissions_not_subset", status_code=403)
        for perm in PERMISSIONS:
            setattr(user, perm, user_dict[perm])


def update_user_username(user: User, user_dict: Dict[str, Any]) -> None:
    """Update username."""
    user.username = user_dict["username"]


def update_user_password(user: User, user_dict: Dict[str, Any]) -> None:
    """Update user password."""
    if "password" in user_dict:
        user.password = generate_password_hash(user_dict["password"])


@bp.route("/<int:user_id>", methods=("DELETE",))
@authentication_required
@requires_permissions("view_users", "update_users")
def delete_user(user_id: int) -> str:
    """Flask view to delete a user with DELETE."""

    user = User.query.get(user_id)
    if user is not None:
        db.session.delete(User.query.get(user_id))
        db.session.commit()

    return str(user_id)


@bp.route("/<int:user_id>", methods=("GET",))
@authentication_required
@requires_permissions("view_users")
def get_user(user_id: int) -> Any:
    """Flask view to get a specified user."""
    user = User.query.get(user_id)
    if user is None:
        raise APIError(reason="no_such_user", status_code=400)
    return UserSchema().dump(user)


@bp.route("/me", methods=("GET",))
@authentication_required
def get_self() -> Any:
    """Flask view to get the current session's user as JSON."""
    self_id = session["user_id"]
    self_user = User.query.get(self_id)
    if self_user is None:
        raise APIError(reason="no_such_user", status_code=400)
    return UserSchema().dump(self_user)


@bp.route("/me", methods=("PUT",))
@authentication_required
def update_self() -> Any:
    """Flask view to update current session's user as JSON."""
    user_schema = UserSchema()
    user_dict = user_schema.load(request.json, partial=("password",))

    if user_dict["id"] != session["user_id"]:
        raise APIError(reason="incorrect_id", status_code=400)

    user = User.query.get(user_dict["id"])
    if user is None:
        raise APIError(reason="no_such_user", status_code=400)

    if user.edit_qualifications:
        update_user_qualifications(user, user_dict)
    elif wants_to_update_qualifications(user, user_dict):
        raise insufficient_permissions()

    if user.update_users:
        update_user_permissions(user, user_dict)
    elif wants_to_update_permissions(user, user_dict):
        raise insufficient_permissions()

    update_user_username(user, user_dict)
    update_user_password(user, user_dict)

    db.session.commit()

    return cast(Dict[str, Any], user_schema.dump(user))


def insufficient_permissions() -> APIError:
    """Return an API error for insufficient permissions."""
    return APIError(reason="insufficient_permissions", status_code=403)


def wants_to_update_qualifications(user: User, user_dict: Dict[str, Any]) -> bool:
    """Check if qualifications need updating."""
    current_qualifications = {q.id for q in user.qualifications}
    new_qualifications = {q["id"] for q in user_dict["qualifications"]}
    return current_qualifications != new_qualifications


def wants_to_update_permissions(user: User, user_dict: Dict[str, Any]) -> bool:
    """Check if permissions need updating."""
    return any(user_dict[p] != getattr(user, p) for p in PERMISSIONS)


@bp.route("/me", methods=("DELETE",))
@authentication_required
def delete_self() -> Any:
    """Flask view to delete current session's user."""
    user_id = session["user_id"]
    user = User.query.get(user_id)
    if user is not None:
        db.session.delete(User.query.get(user_id))
        db.session.commit()

    return logout()


@bp.route("", methods=("GET",))
@authentication_required
@requires_permissions("view_users")
def list_users() -> Dict[str, List[str]]:
    """Flask view to get a list of users using GET."""
    users = UserSchema(many=True).dump(User.query.all())
    return {"users": users}


@click.command("create-user")
@click.option("--username", prompt="Username")
@click.option(
    "--password", prompt="Password", confirmation_prompt=True, hide_input=True
)
@click.option("--create-users", prompt="Permission create_users [y/n]", type=bool)
@click.option("--view-users", prompt="Permission view_users [y/n]", type=bool)
@click.option("--update-users", prompt="Permission update_users [y/n]", type=bool)
@click.option(
    "--edit-qualifications", prompt="Permission edit_qualifications [y/n]", type=bool
)
@click.option("--create-items", prompt="Permission create_items [y/n]", type=bool)
@click.option(
    "--manage-checkouts", prompt="Permission manage_checkouts [y/n]", type=bool
)
@with_appcontext
def create_user_command(**args: Any) -> None:
    """CLI command to create a new user."""
    args["password"] = generate_password_hash(args["password"])
    db.session.add(User(**args))
    db.session.commit()
    click.echo("Created user {}".format(args["username"]))
