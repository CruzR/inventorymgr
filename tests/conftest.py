import datetime
import os
import tempfile

import pytest
from werkzeug.security import generate_password_hash

from inventorymgr import create_app
from inventorymgr.db import db
from inventorymgr.db.models import User, RegistrationToken


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///{}'.format(db_path),
    })

    with app.app_context():
        db.create_all()
        db.session.add(User(username='test', password=generate_password_hash('test'), create_users=True, view_users=True, update_users=True))
        db.session.add(User(username='min_permissions_user', password=generate_password_hash('test')))
        db.session.add(RegistrationToken(token='expired', expires=datetime.datetime(2019, 11, 11)))
        db.session.add(RegistrationToken(token='valid', expires=datetime.datetime(2049, 11, 11)))
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
