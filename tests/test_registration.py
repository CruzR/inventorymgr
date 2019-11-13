import datetime

import pytest
from flask import url_for

from inventorymgr.auth import is_password_correct
from inventorymgr.db.models import RegistrationToken, User
from inventorymgr.registration import (
    registration_url, generate_registration_token,
)


def test_registration_url(app):
    with app.app_context():
        url = registration_url(RegistrationToken(token='test'))
    assert url == 'http://localhost:5000/register/test'


def test_generate_registration_token(app, monkeypatch):
    now = datetime.datetime.now()
    monkeypatch.setattr('secrets.token_hex', lambda: 'test')
    with app.app_context():
        token_obj = generate_registration_token()
        token, expires = token_obj.token, token_obj.expires
    assert token == 'test'
    assert (expires - (now + datetime.timedelta(days=7))) < datetime.timedelta(seconds=5)


def test_generate_registration_token_failure(app, monkeypatch):
    monkeypatch.setattr('secrets.token_hex', lambda: 'valid')
    with pytest.raises(RuntimeError):
        with app.app_context():
            generate_registration_token()


def test_generate_registration_token_command(app, runner, monkeypatch):
    monkeypatch.setattr('secrets.token_hex', lambda: 'test')
    with app.app_context():
        result = runner.invoke(args=['generate-registration-token'])
    assert result.output.strip() == 'http://localhost:5000/register/test'


def test_get_register_view(client):
    response = client.get('/register/test')
    assert b'form' in response.data
    assert b'method="POST"' in response.data
    assert b'name="username"' in response.data
    assert b'name="password"' in response.data
    assert b'name="repeat_password"' in response.data
    assert b'submit' in response.data


@pytest.mark.parametrize(('formdata', 'message'), (
    ({'password': 'test', 'repeat_password': 'test'}, b'username&#34; is required'),
    ({'username': 'test', 'repeat_password': 'test'}, b'password&#34; is required'),
    ({'username': 'test', 'password': 'test'}, b'repeat_password&#34; is required')))
def test_handle_registration_request_missing_field(client, formdata, message):
    response = client.post('/register/test', data=formdata)
    assert response.status_code == 400
    assert message in response.data


def test_handle_registration_request_password_mismatch(client):
    response = client.post(
        '/register/test',
        data={'username': 'test', 'password': 'test', 'repeat_password': 'tes'}
    )
    assert response.status_code == 400
    assert b'Passwords do not match' in response.data


def test_handle_registration_invalid_token(client):
    response = client.post(
        '/register/test',
        data={'username': 'test', 'password': 'test', 'repeat_password': 'test'}
    )
    assert response.status_code == 400
    assert b'Invalid registration token' in response.data


def test_handle_registration_with_expired_token(client):
    response = client.post(
        '/register/expired',
        data={'username': 'test', 'password': 'test', 'repeat_password': 'test'}
    )
    assert response.status_code == 400
    assert b'token has expired' in response.data


def test_handle_registration_with_valid_toke(client, app):
    response = client.post(
        '/register/valid',
        data={'username': 'new_user', 'password': 'abc', 'repeat_password': 'abc'}
    )
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost:5000/register/success'

    with app.app_context():
        assert User.query.filter_by(username='new_user').count() == 1
        assert RegistrationToken.query.filter_by(token='valid').count() == 0
        assert is_password_correct('new_user', 'abc')


def test_handle_registration_with_existing_user(client, app):
    response = client.post(
        '/register/valid',
        data={'username': 'test', 'password': 'abc', 'repeat_password': 'abc'}
    )

    # Need to return the same as with new user to avoid user enumeration
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost:5000/register/success'

    with app.app_context():
        assert User.query.filter_by(username='test').count() == 1
        assert RegistrationToken.query.filter_by(token='valid').count() == 0
        assert not is_password_correct('test', 'abc')


def test_success_or_user_exists(client):
    response = client.get('/register/success')
    assert response.status_code == 200
    assert b'Registration was successful' in response.data
