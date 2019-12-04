from flask import session


def test_login_invalid_user_and_password(client):
    invalid_user = {'username': 'unknow_user', 'password': 'test'}
    invalid_password_user = {'username': 'test', 'password': '123456'}

    with client:
        invalid_user_response = client.post('/api/v1/auth/login', json=invalid_user)
        assert session.get('user') is None
        cookies = {cookie.name: cookie.value for cookie in client.cookie_jar}
        assert cookies.get('is_authenticated') is None

    with client:
        invalid_pw_response = client.post('/api/v1/auth/login', json=invalid_password_user)
        assert session.get('user') is None
        cookies = {cookie.name: cookie.value for cookie in client.cookie_jar}
        assert cookies.get('is_authenticated') is None

    assert invalid_user_response.status_code == 403
    assert invalid_pw_response.status_code == 403
    assert invalid_user_response.is_json
    assert invalid_pw_response.is_json
    assert invalid_user_response.json == invalid_pw_response.json


def test_login_valid_user_and_password(client):
    user = {'username': 'test', 'password': 'test'}

    with client:
        response = client.post('/api/v1/auth/login', json=user)
        assert session.get('user') is not None
        assert session['user']['username'] == user['username']

    assert response.status_code == 200
    assert response.is_json
    assert response.json == {'success': True}
    cookies = {cookie.name: cookie.value for cookie in client.cookie_jar}
    assert cookies.get('is_authenticated') == '1'


def test_logout_when_not_logged_in(client):
    with client:
        response = client.post('/api/v1/auth/logout')
        assert response.status_code == 200
        assert session.get('user') is None

    cookies = {cookie.name: cookie.value for cookie in client.cookie_jar}
    assert cookies.get('is_authenticated') is None


def test_logout_when_logged_in(client):
    client.post('/api/v1/auth/login', json={'username': 'test', 'password': 'test'})

    with client:
        response = client.post('/api/v1/auth/logout')
        assert response.status_code == 200
        assert session.get('user') is None

    cookies = {cookie.name: cookie.value for cookie in client.cookie_jar}
    assert cookies.get('is_authenticated') is None
