import os
import tempfile

import pytest
from werkzeug.security import generate_password_hash

from inventorymgr import create_app
from inventorymgr.db import db
from inventorymgr.db.models import User


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///{}'.format(db_path),
    })

    with app.app_context():
        db.create_all()
        db.session.add(User(username='test', password=generate_password_hash('test'), view_users=True, update_user=True))
        db.session.add(User(username='min_permissions_user', password=generate_password_hash('test')))
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
