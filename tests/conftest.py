import os
import tempfile
from pathlib import Path

import pytest

from inventorymgr import create_app
from inventorymgr.db import get_db, init_db


with open(Path(__file__).parent / 'data.sql') as test_db_sql:
    _TEST_DB_CONTENTS = test_db_sql.read()


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_TEST_DB_CONTENTS)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def authenticated_user(client):
    user = {'username': 'test', 'password': 'test'}
    client.post('/auth/login', json=user)
    return user
