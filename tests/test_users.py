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
        'qualifications': [{'id': 1, 'name': "Driver's License"}],
    }


def test_creating_new_users_unauthenticated(client, app, test_user):
    test_user.update({'username': 'a_new_user', 'password': '123456'})
    response = client.post('/api/v1/users', json=test_user)
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'

    with app.app_context():
        assert count_users_with_name(test_user['username']) == 0


def test_creating_new_users_with_insufficient_permissions(client, app, test_user, auth):
    auth.login('min_permissions_user')
    test_user.update({'username': 'a_new_user', 'password': '123456'})
    response = client.post('/api/v1/users', json=test_user)
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'insufficient_permissions'

    with app.app_context():
        assert count_users_with_name(test_user['username']) == 0


def test_creating_new_users(client, app, test_user, auth):
    auth.login('test')
    test_user.update({'username': 'a_new_user', 'password': '123456'})
    response = client.post('/api/v1/users', json=test_user)
    assert response.status_code == 200
    assert response.is_json
    assert response.json['username'] == 'a_new_user'
    assert response.json['qualifications'] == [{'id': 1, 'name': "Driver's License"}]
    assert response.json['view_users']
    assert 'password' not in response.json

    with app.app_context():
        assert count_users_with_name(test_user['username']) == 1
        assert is_password_correct(test_user['username'], test_user['password'])
        user = User.query.filter_by(username=test_user['username']).first()
        assert user.qualifications[0].id == 1
        assert user.qualifications[0].name == "Driver's License"


def test_creating_new_users_permissions_not_subset(client, app, test_user, auth):
    with app.app_context():
        user = User.query.get(1)
        user.view_users = False
        db.session.commit()

    auth.login('test')
    test_user.update({'username': 'a_new_user', 'password': '123456'})
    response = client.post('/api/v1/users', json=test_user)
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'permissions_not_subset'

    with app.app_context():
        assert count_users_with_name(test_user['username']) == 0


def test_creating_new_unqualified_users_without_edit_qualifications(client, app, test_user, auth):
    with app.app_context():
        user = User.query.get(1)
        user.edit_qualifications = False
        db.session.commit()

    auth.login('test')
    test_user.update({
        'username': 'a_new_user',
        'password': '123456',
        'edit_qualifications': False,
        'qualifications': [],
    })
    response = client.post('/api/v1/users', json=test_user)
    assert response.status_code == 200
    assert response.is_json
    assert response.json['username'] == 'a_new_user'
    assert response.json['qualifications'] == []
    assert response.json['view_users']
    assert not response.json['edit_qualifications']
    assert 'password' not in response.json

    with app.app_context():
        assert count_users_with_name(test_user['username']) == 1
        assert is_password_correct(test_user['username'], test_user['password'])


def test_creating_new_qualified_users_without_edit_qualifications(client, app, test_user, auth):
    with app.app_context():
        user = User.query.get(1)
        user.edit_qualifications = False
        db.session.commit()

    auth.login('test')
    test_user.update({
        'username': 'a_new_user',
        'password': '123456',
        'edit_qualifications': False,
    })
    response = client.post('/api/v1/users', json=test_user)
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'insufficient_permissions'

    with app.app_context():
        assert count_users_with_name(test_user['username']) == 0


def test_creating_existing_user(client, app, test_user, auth):
    auth.login('test')
    test_user.update({'password': '123456'})
    response = client.post('/api/v1/users', json=test_user)
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'user_exists'

    with app.app_context():
        assert count_users_with_name(test_user['username']) == 1
        assert not is_password_correct(test_user['username'], test_user['password'])


def test_updating_user(client, app, test_user, auth):
    auth.login('test')
    test_user['username'] = 'test_1'
    test_user['password'] = '123456'
    response = client.put('/api/v1/users/1', json=test_user)
    assert response.status_code == 200
    assert response.is_json
    assert response.json['username'] == 'test_1'
    assert response.json['qualifications'] == [{'id': 1, 'name': "Driver's License"}]
    assert response.json['view_users']
    assert 'password' not in response.json

    with app.app_context():
        assert count_users_with_name('test') == 0
        assert count_users_with_name(test_user['username']) == 1
        assert is_password_correct(test_user['username'], test_user['password'])


def test_updating_user_permissions_not_subset(client, app, test_user, auth):
    with app.app_context():
        user = User.query.get(1)
        user.edit_qualifications = False
        db.session.commit()

    auth.login('test')
    test_user.update({'password': '123456'})
    response = client.put('/api/v1/users/1', json=test_user)
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'permissions_not_subset'

    with app.app_context():
        user = User.query.get(1)
        assert not user.edit_qualifications
        assert not is_password_correct(test_user['username'], test_user['password'])


def test_updating_user_permissions_subset(client, app, test_user, auth):
    with app.app_context():
        user = User.query.get(1)
        user.edit_qualifications = False
        db.session.commit()

    auth.login('test')
    test_user.update({
        'password': '123456',
        'edit_qualifications': False,
        'update_users': False,
    })
    response = client.put('/api/v1/users/1', json=test_user)
    assert response.status_code == 200
    assert response.is_json
    assert response.json['username'] == 'test'
    assert response.json['qualifications'] == [{'id': 1, 'name': "Driver's License"}]
    assert response.json['view_users']
    assert not response.json['edit_qualifications']
    assert 'password' not in response.json

    with app.app_context():
        user = User.query.get(1)
        assert not user.edit_qualifications
        assert not user.update_users
        assert is_password_correct(test_user['username'], test_user['password'])


def test_updating_user_with_more_permissions(client, app, test_user, auth):
    with app.app_context():
        user = User.query.get(2)
        user.view_users = True
        user.update_users = True
        db.session.commit()

    auth.login('min_permissions_user')
    test_user.update({
        'username': 'changed',
    })
    response = client.put('/api/v1/users/1', json=test_user)
    assert response.status_code == 200
    assert response.is_json
    assert response.json['username'] == 'changed'
    assert response.json['qualifications'] == [{'id': 1, 'name': "Driver's License"}]
    assert response.json['view_users']
    assert response.json['edit_qualifications']
    assert 'password' not in response.json

    with app.app_context():
        assert count_users_with_name('test') == 0
        assert count_users_with_name(test_user['username']) == 1


def test_updating_user_unauthenticated(client, app, test_user):
    test_user['password'] = '123456'
    response = client.put('/api/v1/users/1', json=test_user)
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'

    with app.app_context():
        assert count_users_with_name(test_user['username']) == 1
        assert not is_password_correct(test_user['username'], test_user['password'])


def test_updating_user_with_insufficient_permissions(client, app, test_user, auth):
    auth.login('min_permissions_user')
    test_user['password'] = '123456'
    response = client.put('/api/v1/users/1', json=test_user)
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'insufficient_permissions'

    with app.app_context():
        assert count_users_with_name(test_user['username']) == 1
        assert not is_password_correct(test_user['username'], test_user['password'])


def test_updating_user_with_incorrect_id(client, app, test_user, auth):
    auth.login('test')
    test_user.update({'id': 2, 'username': 'a_new_user', 'password': '123456'})
    response = client.put('/api/v1/users/1', json=test_user)
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'incorrect_id'

    with app.app_context():
        assert count_users_with_name(test_user['username']) == 0


def test_updating_nonexistant_user(client, app, test_user, auth):
    auth.login('test')
    test_user.update({'id': 3, 'username': 'a_new_user', 'password': '123456'})
    response = client.put('/api/v1/users/3', json=test_user)
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'no_such_user'

    with app.app_context():
        assert count_users_with_name(test_user['username']) == 0


def test_updating_unqualified_users_without_edit_qualifications(client, app, test_user, auth):
    with app.app_context():
        user = User.query.get(1)
        user.edit_qualifications = False
        db.session.commit()

    auth.login('test')
    test_user.update({
        'id': 2,
        'username': 'changed',
        'create_users': False,
        'view_users': False,
        'update_users': False,
        'edit_qualifications': False,
        'qualifications': [],
    })
    response = client.put('/api/v1/users/2', json=test_user)
    assert response.status_code == 200
    assert response.is_json
    assert response.json['username'] == 'changed'
    assert response.json['qualifications'] == []
    assert not response.json['view_users']
    assert not response.json['edit_qualifications']
    assert 'password' not in response.json

    with app.app_context():
        assert count_users_with_name('min_permissions_user') == 0
        assert count_users_with_name(test_user['username']) == 1


def test_updating_qualified_users_without_edit_qualifications(client, app, test_user, auth):
    with app.app_context():
        user = User.query.get(1)
        user.edit_qualifications = False
        db.session.commit()

    auth.login('test')
    test_user.update({
        'id': 2,
        'username': 'changed',
        'create_users': False,
        'view_users': False,
        'update_users': False,
        'edit_qualifications': False,
    })
    response = client.put('/api/v1/users/2', json=test_user)
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'insufficient_permissions'

    with app.app_context():
        assert count_users_with_name('min_permissions_user') == 1
        assert count_users_with_name(test_user['username']) == 0


def test_updating_qualified_users_with_edit_qualifications(client, app, test_user, auth):
    auth.login('test')
    test_user.update({
        'id': 2,
        'username': 'changed',
        'create_users': False,
        'view_users': False,
        'update_users': False,
        'edit_qualifications': False,
        'qualifications': [{'id': 1, 'name': "Driver's License"}],
    })
    response = client.put('/api/v1/users/2', json=test_user)
    assert response.status_code == 200
    assert response.is_json
    assert response.json['username'] == 'changed'
    assert response.json['qualifications'] == [{'id': 1, 'name': "Driver's License"}]
    assert not response.json['view_users']
    assert not response.json['edit_qualifications']
    assert 'password' not in response.json

    with app.app_context():
        assert count_users_with_name('min_permissions_user') == 0
        assert count_users_with_name(test_user['username']) == 1
        user = User.query.get(test_user['id'])
        assert len(user.qualifications) == 1


def test_list_users(client, auth):
    auth.login('test')
    response = client.get('/api/v1/users')
    assert response.status_code == 200
    assert response.is_json
    usernames = {u['username'] for u in response.json['users']}
    assert usernames == {'test', 'min_permissions_user'}
    assert not any('password' in u for u in response.json['users'])


def test_list_users_unauthenticated(client):
    response = client.get('/api/v1/users')
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'


def test_list_users_with_insufficient_permissions(client, auth):
    auth.login('min_permissions_user')
    response = client.get('/api/v1/users')
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'insufficient_permissions'


def test_delete_user_unauthenticated(client, app):
    response = client.delete('/api/v1/users/2')
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'

    with app.app_context():
        assert User.query.get(2) is not None


def test_delete_user_with_insufficient_permissions(client, app, auth):
    auth.login('min_permissions_user')
    response = client.delete('/api/v1/users/1')
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'insufficient_permissions'

    with app.app_context():
        assert User.query.get(1) is not None


def test_delete_user(client, app, auth):
    auth.login('test')
    response = client.delete('/api/v1/users/2')
    assert response.status_code == 200

    with app.app_context():
        assert User.query.get(2) is None


def test_delete_user_but_user_does_not_exist(client, app, auth):
    auth.login('test')
    response = client.delete('/api/v1/users/3')
    assert response.status_code == 200

    with app.app_context():
        assert User.query.get(3) is None


def test_create_user_command(runner, app):
    result = runner.invoke(args=[
        'create-user',
        '--username', 'test2',
        '--password', '123456',
        '--create-users', 'no',
        '--view-users', 'yes',
        '--update-users=1',
        '--edit-qualifications', 'false',
    ])
    assert 'Created user' in result.output

    with app.app_context():
        user = User.query.filter_by(username='test2').first()
        assert user is not None
        assert is_password_correct('test2', '123456')
        assert not user.create_users
        assert user.view_users
        assert user.update_users
        assert not user.edit_qualifications


def count_users_with_name(username):
    return User.query.filter_by(username=username).count()
