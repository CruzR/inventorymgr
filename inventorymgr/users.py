"""
User management views.

new_user()
    Flask view to create a new user using POST.

update_user()
    Flask view to update a user using PUT.

list_users()
    Flask view to get a list of users using GET.
"""

from typing import Any, Dict, List

import click
from flask import Blueprint, request, session
from flask.cli import with_appcontext
from sqlalchemy.exc import IntegrityError  # type: ignore
from werkzeug.security import generate_password_hash

from inventorymgr import api, service
from inventorymgr.accesscontrol import requires_permissions
from inventorymgr.api import APIError
from inventorymgr.auth import authentication_required, logout
from inventorymgr.db import db
from inventorymgr.db.models import User


bp = Blueprint("users", __name__, url_prefix="/api/v1/users")


@bp.route("", methods=("POST",))
@authentication_required
@requires_permissions("create_users")
def new_user() -> Dict[str, Any]:
    """Flask view to create a new user using POST."""
    user_obj = api.NewUser.parse_obj(request.json)

    try:
        user = service.create_user(user_obj)
        return api.User.from_orm(user).dict()
    except IntegrityError as exc:
        raise APIError(reason="user_exists", status_code=400) from exc


@bp.route("/<int:user_id>", methods=("PUT",))
@authentication_required
@requires_permissions("update_users")
def update_user(user_id: int) -> Dict[str, Any]:
    """Flask view to update a user using PUT."""
    user_obj = api.UpdatedUser.parse_obj(request.json)
    user = service.update_user(user_id, user_obj)
    return api.User.from_orm(user).dict()


@bp.route("/<int:user_id>", methods=("DELETE",))
@authentication_required
@requires_permissions("update_users")
def delete_user(user_id: int) -> str:
    """Flask view to delete a user with DELETE."""
    service.delete_user(user_id)
    return str(user_id)


@bp.route("/<int:user_id>", methods=("GET",))
@authentication_required
def get_user(user_id: int) -> Any:
    """Flask view to get a specified user."""
    user = service.read_user(user_id)
    return api.User.from_orm(user).dict()


@bp.route("/me", methods=("GET",))
@authentication_required
def get_self() -> Any:
    """Flask view to get the current session's user as JSON."""
    self_id = session["user_id"]
    self_user = service.read_user(self_id)
    return api.User.from_orm(self_user).dict()


@bp.route("/me", methods=("PUT",))
@authentication_required
def update_self() -> Any:
    """Flask view to update current session's user as JSON."""
    user_obj = api.UpdatedUser.parse_obj(request.json)
    user = service.update_session_user(session["user_id"], user_obj)
    return api.User.from_orm(user).dict()


@bp.route("/me", methods=("DELETE",))
@authentication_required
def delete_self() -> Any:
    """Flask view to delete current session's user."""
    user_id = session["user_id"]
    service.delete_user(user_id)
    return logout()


@bp.route("", methods=("GET",))
@authentication_required
def list_users() -> Dict[str, List[str]]:
    """Flask view to get a list of users using GET."""
    users = list(service.iterate_users())
    return api.UserCollection(users=users).dict()


@click.command("create-user")
@click.option("--username", prompt="Username")
@click.option(
    "--password", prompt="Password", confirmation_prompt=True, hide_input=True
)
@click.option("--create-users", prompt="Permission create_users [y/n]", type=bool)
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
