"""Database ORM models. """

import datetime

from . import db


# pylint: disable=too-few-public-methods

class User(db.Model): # type: ignore

    """ORM model for user objects."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    view_users = db.Column(db.Boolean, nullable=False, default=False)
    update_user = db.Column(db.Boolean, nullable=False, default=False)


class RegistrationToken(db.Model): # type: ignore

    """ORM model for registration tokens."""

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, unique=True, nullable=False)
    expires = db.Column(db.TIMESTAMP, nullable=False, default=datetime.datetime.now)
