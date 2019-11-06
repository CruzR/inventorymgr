from werkzeug.security import check_password_hash

from inventorymgr.db import get_db


def test_creating_new_users(client, app):
    user = {'username': 'a_new_user', 'password': '123456'}
    response = client.post('/users/', json=user)
    assert response.status_code == 200
    assert response.is_json
    assert response.json == {'success': True}

    with app.app_context():
        assert count_users_with_name(user['username']) == 1
        password = password_for_user(user['username'])
        assert check_password_hash(password, user['password'])


def test_creating_existing_user(client, app):
    user = {'username': 'test', 'password': '123456'}
    response = client.post('/users/', json=user)
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'user_exists'

    with app.app_context():
        assert count_users_with_name(user['username']) == 1
        password = password_for_user(user['username'])
        assert not check_password_hash(password, user['password'])


def test_updating_user(client, app):
    user = {'username': 'test', 'password': '123456'}
    response = client.put('/users/', json=user)
    assert response.status_code == 200
    assert response.is_json
    assert response.json == {'success': True}

    with app.app_context():
        assert count_users_with_name(user['username']) == 1
        password = password_for_user(user['username'])
        assert check_password_hash(password, user['password'])


def test_updating_nonexistant_user(client, app):
    user = {'username': 'a_new_user', 'password': '123456'}
    response = client.put('/users/', json=user)
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'no_such_user'

    with app.app_context():
        assert count_users_with_name(user['username']) == 0


def test_list_users(client):
    response = client.get('/users/')
    assert response.status_code == 200
    assert response.is_json
    assert response.json == {'users': ['test']}


def count_users_with_name(username):
    return get_db().execute(
        'SELECT COUNT(*) FROM users WHERE username = ?',
        (username,)
    ).fetchone()[0]


def password_for_user(username):
    return get_db().execute(
        'SELECT password FROM users WHERE username = ?',
        (username,)
    ).fetchone()['password']
