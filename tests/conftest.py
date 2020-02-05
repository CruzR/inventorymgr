import datetime
import os
import tempfile

import pytest
from werkzeug.security import generate_password_hash

from inventorymgr import create_app
from inventorymgr.db import db
from inventorymgr.db.models import (
    User,
    Qualification,
    RegistrationToken,
    BorrowableItem,
    BorrowState,
    LogEntry,
)


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///{}".format(db_path),}
    )

    with app.app_context():
        db.create_all()
        all_permissions_user = User(
            username="test",
            password=generate_password_hash("test"),
            create_users=True,
            view_users=True,
            update_users=True,
            edit_qualifications=True,
            create_items=True,
            manage_checkouts=True,
        )
        db.session.add(all_permissions_user)
        min_permissions_user = User(
            username="min_permissions_user", password=generate_password_hash("test")
        )
        db.session.add(min_permissions_user)
        db.session.add(
            RegistrationToken(token="expired", expires=datetime.datetime(2019, 11, 11))
        )
        db.session.add(
            RegistrationToken(token="valid", expires=datetime.datetime(2049, 11, 11))
        )
        drivers_license = Qualification(name="Driver's License")
        all_permissions_user.qualifications = [drivers_license]
        db.session.add(drivers_license)
        db.session.add(
            BorrowableItem(
                name="existing_item", required_qualifications=[drivers_license]
            )
        )
        db.session.add(
            BorrowableItem(
                name="another_item", required_qualifications=[drivers_license]
            )
        )
        db.session.add(
            BorrowState(
                borrowing_user_id=1,
                borrowed_item_id=1,
                received_at=datetime.datetime(2020, 1, 2, 12, 34, 56),
            )
        )
        db.session.add(
            LogEntry(
                timestamp=datetime.datetime(2020, 1, 2, 12, 34, 56),
                action="checkout",
                subject_id=1,
                items=[BorrowableItem.query.get(1)],
            )
        )
        db.session.commit()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthenticationManager:
    def __init__(self, client):
        self.client = client

    def login(self, username):
        user = {"username": username, "password": "test"}
        self.client.post("/api/v1/auth/login", json=user)


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
