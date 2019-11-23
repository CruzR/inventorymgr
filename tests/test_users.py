import pytest

from inventorymgr.auth import is_password_correct
from inventorymgr.db import db
from inventorymgr.db.models import User


@pytest.fixture
def test_user():
    return {
        'id': 1,
        'username': 'test',
        'password': 'test',
        'create_users': True,
        'view_users': True,
        'update_users': True,
        'edit_qualifications': True,
    }


def test_creating_new_users_unauthenticated(client, app, test_user):
    test_user.update({'username': 'a_new_user', 'password': '123456'})
    response = client.post('/users', json=test_user)
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'

    with app.app_context():
        assert count_users_with_name(test_user['username']) == 0


def test_creating_new_users_with_insufficient_permissions(client, app, test_user):
    authenticate_user(client, 'min_permissions_user')
    test_user.update({'username': 'a_new_user', 'password': '123456'})
    response = client.post('/users', json=test_user)
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'insufficient_permissions'

    with app.app_context():
        assert count_users_with_name(test_user['username']) == 0


def test_creating_new_users(client, app, test_user):
    authenticate_user(client, 'test')
    test_user.update({'username': 'a_new_user', 'password': '123456'})
    response = client.post('/users', json=test_user)
    assert response.status_code == 200
    assert response.is_json
    assert response.json == {'success': True}

    with app.app_context():
        assert count_users_with_name(test_user['username']) == 1
        assert is_password_correct(test_user['username'], test_user['password'])


def test_creating_new_users_permissions_not_subset(client, app, test_user):
    with app.app_context():
        user = User.query.get(1)
        user.edit_qualifications = False
        db.session.commit()

    authenticate_user(client, 'test')
    test_user.update({'username': 'a_new_user', 'password': '123456'})
    response = client.post('/users', json=test_user)
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'permissions_not_subset'

    with app.app_context():
        assert count_users_with_name(test_user['username']) == 0


def test_creating_existing_user(client, app, test_user):
    authenticate_user(client, 'test')
    test_user.update({'password': '123456'})
    response = client.post('/users', json=test_user)
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'user_exists'

    with app.app_context():
        assert count_users_with_name(test_user['username']) == 1
        assert not is_password_correct(test_user['username'], test_user['password'])


def test_updating_user(client, app, test_user):
    authenticate_user(client, 'test')
    test_user['username'] = 'test_1'
    test_user['password'] = '123456'
    response = client.put('/users/1', json=test_user)
    assert response.status_code == 200
    assert response.is_json
    assert response.json == {'success': True}

    with app.app_context():
        assert count_users_with_name('test') == 0
        assert count_users_with_name(test_user['username']) == 1
        assert is_password_correct(test_user['username'], test_user['password'])


def test_updating_user_permissions_not_subset(client, app, test_user):
    with app.app_context():
        user = User.query.get(1)
        user.edit_qualifications = False
        db.session.commit()

    authenticate_user(client, 'test')
    response = client.put('/users/1', json=test_user)
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'permissions_not_subset'

    with app.app_context():
        user = User.query.get(1)
        assert not user.edit_qualifications


def test_updating_user_unauthenticated(client, app, test_user):
    test_user['password'] = '123456'
    response = client.put('/users/1', json=test_user)
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'

    with app.app_context():
        assert count_users_with_name(test_user['username']) == 1
        assert not is_password_correct(test_user['username'], test_user['password'])


def test_updating_user_with_insufficient_permissions(client, app, test_user):
    authenticate_user(client, 'min_permissions_user')
    test_user['password'] = '123456'
    response = client.put('/users/1', json=test_user)
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'insufficient_permissions'

    with app.app_context():
        assert count_users_with_name(test_user['username']) == 1
        assert not is_password_correct(test_user['username'], test_user['password'])


def test_updating_user_with_incorrect_id(client, app, test_user):
    authenticate_user(client, 'test')
    test_user.update({'id': 2, 'username': 'a_new_user', 'password': '123456'})
    response = client.put('/users/1', json=test_user)
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'incorrect_id'

    with app.app_context():
        assert count_users_with_name(test_user['username']) == 0


def test_updating_nonexistant_user(client, app, test_user):
    authenticate_user(client, 'test')
    test_user.update({'id': 3, 'username': 'a_new_user', 'password': '123456'})
    response = client.put('/users/3', json=test_user)
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'no_such_user'

    with app.app_context():
        assert count_users_with_name(test_user['username']) == 0


def test_list_users(client):
    authenticate_user(client, 'test')
    response = client.get('/users')
    assert response.status_code == 200
    assert response.is_json
    usernames = {u['username'] for u in response.json['users']}
    assert usernames == {'test', 'min_permissions_user'}
    assert not any('password' in u for u in response.json['users'])


def test_list_users_unauthenticated(client):
    response = client.get('/users')
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'


def test_list_users_with_insufficient_permissions(client):
    authenticate_user(client, 'min_permissions_user')
    response = client.get('/users')
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'insufficient_permissions'


def count_users_with_name(username):
    return User.query.filter_by(username=username).count()


def authenticate_user(client, username):
    user = {'username': username, 'password': 'test'}
    client.post('/auth/login', json=user)
