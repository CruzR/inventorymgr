import datetime

import pytest
from flask import url_for

from inventorymgr.auth import is_password_correct
from inventorymgr.db.models import RegistrationToken, User
from inventorymgr.registration import generate_registration_token


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
    assert result.output.strip() == 'test'


@pytest.mark.parametrize(('json', 'field'), (
    ({'password': 'test', 'repeat_password': 'test'}, 'username'),
    ({'username': 'test', 'repeat_password': 'test'}, 'password'),
    ({'username': 'test', 'password': 'test'}, 'repeat_password')))
def test_handle_registration_request_missing_field(client, json, field):
    response = client.post('/api/v1/registration/test', json=json)
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'missing_fields'
    assert field in response.json['missing']


def test_handle_registration_request_password_mismatch(client):
    response = client.post(
        '/api/v1/registration/test',
        json={'username': 'test', 'password': 'test', 'repeat_password': 'tes'}
    )
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'password_mismatch'


def test_handle_registration_invalid_token(client):
    response = client.post(
        '/api/v1/registration/test',
        json={'username': 'test', 'password': 'test', 'repeat_password': 'test'}
    )
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'invalid_token'


def test_handle_registration_with_expired_token(client):
    response = client.post(
        '/api/v1/registration/expired',
        json={'username': 'test', 'password': 'test', 'repeat_password': 'test'}
    )
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'expired_token'


def test_handle_registration_with_valid_toke(client, app):
    response = client.post(
        '/api/v1/registration/valid',
        json={'username': 'new_user', 'password': 'abc', 'repeat_password': 'abc'}
    )
    assert response.status_code == 200
    assert response.is_json
    assert response.json['success']

    with app.app_context():
        assert User.query.filter_by(username='new_user').count() == 1
        assert RegistrationToken.query.filter_by(token='valid').count() == 0
        assert is_password_correct('new_user', 'abc')


def test_handle_registration_with_existing_user(client, app):
    response = client.post(
        '/api/v1/registration/valid',
        json={'username': 'test', 'password': 'abc', 'repeat_password': 'abc'}
    )

    # Need to return the same as with new user to avoid user enumeration
    assert response.status_code == 200
    assert response.is_json
    assert response.json['success']

    with app.app_context():
        assert User.query.filter_by(username='test').count() == 1
        assert RegistrationToken.query.filter_by(token='valid').count() == 0
        assert not is_password_correct('test', 'abc')


def test_get_tokens_unauthenticated(client):
    response = client.get('/api/v1/registration/tokens')
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'


def test_get_tokens_with_insufficient_permissions(client, auth):
    auth.login('min_permissions_user')
    response = client.get('/api/v1/registration/tokens')
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'insufficient_permissions'


def test_get_tokens_success(client, auth):
    auth.login('test')
    response = client.get('/api/v1/registration/tokens')
    assert response.status_code == 200
    assert response.is_json
    assert response.json['tokens'] == [
        {'id': 1, 'token': 'expired', 'expires': '2019-11-11T00:00:00'},
        {'id': 2, 'token': 'valid', 'expires': '2049-11-11T00:00:00'},
    ]
