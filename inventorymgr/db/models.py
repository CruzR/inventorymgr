"""Database ORM models. """

import datetime

from . import db


# pylint: disable=too-few-public-methods


_USER_QUALIFICATIONS_TABLE = db.Table(
    "user_qualifications",
    db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("qualification_id", db.Integer, db.ForeignKey("qualification.id")),
)

_REQUIRED_QUALIFICATIONS_TABLE = db.Table(
    "required_qualifications",
    db.Model.metadata,
    db.Column("item_id", db.Integer, db.ForeignKey("borrowable_item.id")),
    db.Column("qualification_id", db.Integer, db.ForeignKey("qualification.id")),
)

_LOGENTRY_ITEMS_TABLE = db.Table(
    "logentry_items",
    db.Model.metadata,
    db.Column("logentry_id", db.Integer, db.ForeignKey("log_entry.id")),
    db.Column("item_id", db.Integer, db.ForeignKey("borrowable_item.id")),
)


class User(db.Model):  # type: ignore

    """ORM model for user objects."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    create_users = db.Column(db.Boolean, nullable=False, default=False)
    view_users = db.Column(db.Boolean, nullable=False, default=False)
    update_users = db.Column(db.Boolean, nullable=False, default=False)
    edit_qualifications = db.Column(db.Boolean, nullable=False, default=False)
    create_items = db.Column(db.Boolean, nullable=False, default=False)
    manage_checkouts = db.Column(db.Boolean, nullable=False, default=False)
    qualifications = db.relationship(
        "Qualification", secondary=_USER_QUALIFICATIONS_TABLE, back_populates="users"
    )
    borrowstates = db.relationship(
        "BorrowState",
        back_populates="borrowing_user",
        cascade="all, delete, delete-orphan",
    )
    log_entries = db.relationship(
        "LogEntry", back_populates="subject", cascade="all, delete, delete-orphan"
    )


class RegistrationToken(db.Model):  # type: ignore

    """ORM model for registration tokens."""

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, unique=True, nullable=False)
    expires = db.Column(db.TIMESTAMP, nullable=False, default=datetime.datetime.now)


class Qualification(db.Model):  # type: ignore

    """ORM model for user qualifications (e.g. driver's license)."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    users = db.relationship(
        "User", secondary=_USER_QUALIFICATIONS_TABLE, back_populates="qualifications"
    )
    items = db.relationship(
        "BorrowableItem",
        secondary=_REQUIRED_QUALIFICATIONS_TABLE,
        back_populates="required_qualifications",
    )


class BorrowableItem(db.Model):  # type: ignore

    """ORM model for borrowable items (tools, vehicles, ...)."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    required_qualifications = db.relationship(
        "Qualification",
        secondary=_REQUIRED_QUALIFICATIONS_TABLE,
        back_populates="items",
    )
    borrowstates = db.relationship(
        "BorrowState",
        back_populates="borrowed_item",
        cascade="all, delete, delete-orphan",
    )
    log_entries = db.relationship(
        "LogEntry", secondary=_LOGENTRY_ITEMS_TABLE, back_populates="items"
    )


class BorrowState(db.Model):  # type: ignore
    """ORM model for borrow state of items."""

    id = db.Column(db.Integer, primary_key=True)
    borrowing_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    borrowing_user = db.relationship("User", back_populates="borrowstates")
    borrowed_item_id = db.Column(
        db.Integer, db.ForeignKey("borrowable_item.id"), nullable=False
    )
    borrowed_item = db.relationship("BorrowableItem", back_populates="borrowstates")
    received_at = db.Column(db.DateTime, nullable=False)
    returned_at = db.Column(db.DateTime)


class JavascriptError(db.Model):  # type: ignore
    """ORM model for storing JS errors sent from window.onerror."""

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    user_agent_raw = db.Column(db.String, nullable=False)
    platform = db.Column(db.String)
    browser = db.Column(db.String)
    browser_version = db.Column(db.String)
    browser_language = db.Column(db.String)
    location = db.Column(db.String, nullable=False)
    message = db.Column(db.String)
    source = db.Column(db.String)
    lineno = db.Column(db.Integer)
    colno = db.Column(db.Integer)
    stack = db.Column(db.String)


class LogEntry(db.Model):  # type: ignore
    """ORM model for checkout / checkin logs."""

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    action = db.Column(db.String, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    subject = db.relationship("User", back_populates="log_entries")
    items = db.relationship(
        "BorrowableItem", back_populates="log_entries", secondary=_LOGENTRY_ITEMS_TABLE
    )
