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
        'create_items': True,
        'manage_checkouts': True,
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


def test_updating_user(client, app, test_user, auth):
    auth.login('test')
    test_user['username'] = 'test_1'
    del test_user['password']
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
        assert is_password_correct(test_user['username'], 'test')


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
        '--create-items=0',
        '--manage-checkouts=1',
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
        assert not user.create_items
        assert user.manage_checkouts


def test_get_me_unauthenticated(client):
    response = client.get('/api/v1/users/me')
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'


def test_get_me(client, auth):
    auth.login('test')
    response = client.get('/api/v1/users/me')
    assert response.status_code == 200
    assert response.is_json
    assert response.json['username'] == 'test'
    assert response.json['id'] == 1


def test_update_self_unauthenticated(client, app):
    response = client.put('/api/v1/users/me', json={
        'id': 1,
        'username': 'other_user',
        'create_users': False,
        'view_users': False,
        'update_users': False,
        'edit_qualifications': False,
        'create_items': False,
        'manage_checkouts': False,
        'qualifications': []
    })
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'


def test_abuse_update_self_to_update_other_user(client, app, auth):
    auth.login('min_permissions_user')
    response = client.put('/api/v1/users/me', json={
        'id': 1,
        'username': 'other_user',
        'create_users': False,
        'view_users': False,
        'update_users': False,
        'edit_qualifications': False,
        'create_items': False,
        'manage_checkouts': False,
        'qualifications': []
    })
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'incorrect_id'

    with app.app_context():
        assert User.query.filter_by(username='test').count() == 1
        assert User.query.filter_by(username='other_user').count() == 0


def test_update_self_username(client, app, auth):
    auth.login('min_permissions_user')
    response = client.put('/api/v1/users/me', json={
        'id': 2,
        'username': 'other_user',
        'create_users': False,
        'view_users': False,
        'update_users': False,
        'edit_qualifications': False,
        'create_items': False,
        'manage_checkouts': False,
        'qualifications': []
    })
    assert response.status_code == 200
    assert response.is_json
    assert response.json['username'] == 'other_user'

    with app.app_context():
        assert User.query.filter_by(username='min_permissions_user').count() == 0
        assert User.query.filter_by(username='other_user').count() == 1


def test_update_self_password(client, app, auth):
    auth.login('min_permissions_user')
    response = client.put('/api/v1/users/me', json={
        'id': 2,
        'username': 'min_permissions_user',
        'password': 'a_new_password',
        'create_users': False,
        'view_users': False,
        'update_users': False,
        'edit_qualifications': False,
        'create_items': False,
        'manage_checkouts': False,
        'qualifications': []
    })
    assert response.status_code == 200
    assert response.is_json
    assert response.json['username'] == 'min_permissions_user'
    assert 'password' not in response.json

    with app.app_context():
        assert is_password_correct('min_permissions_user', 'a_new_password')


def test_update_self_set_permissions_fail(client, app, auth):
    auth.login('min_permissions_user')
    response = client.put('/api/v1/users/me', json={
        'id': 2,
        'username': 'min_permissions_user',
        'create_users': False,
        'view_users': False,
        'update_users': True,
        'edit_qualifications': False,
        'create_items': False,
        'manage_checkouts': False,
        'qualifications': []
    })
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'insufficient_permissions'

    with app.app_context():
        assert not User.query.get(2).update_users


def test_update_self_set_permissions_and_qualifications(client, app, auth):
    auth.login('test')
    response = client.put('/api/v1/users/me', json={
        'id': 1,
        'username': 'test',
        'create_users': True,
        'view_users': True,
        'update_users': True,
        'edit_qualifications': False,
        'create_items': False,
        'manage_checkouts': False,
        'qualifications': [{'id': 1, 'name': "Driver's License"}]
    })
    assert response.status_code == 200
    assert response.is_json
    assert response.json['username'] == 'test'
    assert not response.json['edit_qualifications']

    with app.app_context():
        assert not User.query.get(2).edit_qualifications


def test_update_self_give_more_qualifications_fail(client, app, auth):
    auth.login('min_permissions_user')
    response = client.put('/api/v1/users/me', json={
        'id': 2,
        'username': 'min_permissions_user',
        'create_users': False,
        'view_users': False,
        'update_users': False,
        'edit_qualifications': False,
        'create_items': False,
        'manage_checkouts': False,
        'qualifications': [{'id': 1, 'name': "Driver's License"}]
    })
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'insufficient_permissions'

    with app.app_context():
        assert User.query.get(2).qualifications == []


def test_delete_self_unauthenticated(client, app):
    response = client.delete('/api/v1/users/me')
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'


def test_delete_self(client, app, auth):
    auth.login('min_permissions_user')
    response = client.delete('/api/v1/users/me')
    assert response.status_code == 200
    assert response.is_json
    assert response.json['success']

    with app.app_context():
        assert User.query.filter_by(username='min_permissions_user').count() == 0

    # Deleting yourself should log yourself out
    cookies = {cookie.name: cookie.value for cookie in client.cookie_jar}
    assert cookies.get('session') is None
    assert cookies.get('is_authenticated') is None


def test_deleted_user_logged_out_on_next_request(client, auth, app):
    # User logs in
    auth.login('min_permissions_user')

    with app.app_context():
        # User is deleted in meantime
        db.session.delete(User.query.get(2))
        db.session.commit()

    # User makes an request that requires authentication
    response = client.get('/api/v1/users/me')
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'
    cookies = {cookie.name: cookie.value for cookie in client.cookie_jar}
    assert cookies.get('session') is None
    assert cookies.get('is_authenticated') is None


def count_users_with_name(username):
    return User.query.filter_by(username=username).count()
