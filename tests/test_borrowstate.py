import datetime

import pytest

from inventorymgr.db.models import BorrowState


def test_fetch_borrowstates_unauthenticated(client):
    response = client.get('/api/v1/borrowstates')
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'
    assert 'message' in response.json


def test_fetch_borrowstates_insufficient_permissions(client, auth):
    auth.login('min_permissions_user')
    response = client.get('/api/v1/borrowstates')
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'insufficient_permissions'
    assert 'message' in response.json


def test_fetch_borrowstates_success(client, auth):
    auth.login('test')
    response = client.get('/api/v1/borrowstates')
    assert response.status_code == 200
    assert response.is_json
    assert response.json['borrowstates'] == [{
        'id': 1,
        'borrowing_user': {'id': 1, 'username': 'test'},
        'borrowed_item': {'id': 1, 'name': 'existing_item', 'barcode': '0000000000001'},
        'received_at': '2020-01-02T12:34:56',
        'returned_at': None
    }]


@pytest.fixture
def checkout_request():
    return {
        'borrowing_user_id': 2,
        'borrowed_item_ids': [1],
    }


def test_checkout_unauthenticated(client, checkout_request):
    response = client.post('/api/v1/borrowstates/checkout', json=checkout_request)
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'


def test_checkout_insufficient_permissions(client, auth, checkout_request):
    auth.login('min_permissions_user')
    response = client.post('/api/v1/borrowstates/checkout', json=checkout_request)
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'insufficient_permissions'


def test_checkout_missing_qualifications(client, auth, checkout_request):
    auth.login('test')
    response = client.post('/api/v1/borrowstates/checkout', json=checkout_request)
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'missing_qualifications'


def test_checkout_successful(client, auth, checkout_request, monkeypatch, app):
    def fake_utcnow():
        return datetime.datetime(2020, 1, 4, 13, 37)
    monkeypatch.setattr('inventorymgr.borrowstates._utcnow', fake_utcnow)
    auth.login('test')
    checkout_request['borrowing_user_id'] = 1
    response = client.post('/api/v1/borrowstates/checkout', json=checkout_request)
    assert response.status_code == 200
    assert response.is_json
    assert response.json['borrowstates'] == [{
        'id': 2,
        'borrowing_user': {'id': 1, 'username': 'test'},
        'borrowed_item': {'id': 1, 'name': 'existing_item', 'barcode': '0000000000001'},
        'received_at': '2020-01-04T13:37:00',
        'returned_at': None,
    }]


@pytest.fixture
def checkin_request():
    return {'item_ids': [1]}


def test_checkin_unauthenticated(client, checkin_request):
    response = client.post('/api/v1/borrowstates/checkin', json=checkin_request)
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'


def test_checkin_insufficient_permissions(client, auth, checkin_request):
    auth.login('min_permissions_user')
    response = client.post('/api/v1/borrowstates/checkin', json=checkin_request)
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'insufficient_permissions'


def test_checkin_successful(client, auth, checkin_request, app, monkeypatch):
    def fake_utcnow():
        return datetime.datetime(2020, 1, 6, 13, 37, 42)
    monkeypatch.setattr('inventorymgr.borrowstates._utcnow', fake_utcnow)

    auth.login('test')
    response = client.post('/api/v1/borrowstates/checkin', json=checkin_request)
    assert response.status_code == 200
    assert response.is_json
    assert response.json['borrowstates'] == [{
        'id': 1,
        'borrowing_user': {'id': 1, 'username': 'test'},
        'borrowed_item': {'id': 1, 'name': 'existing_item', 'barcode': '0000000000001'},
        'received_at': '2020-01-02T12:34:56',
        'returned_at': '2020-01-06T13:37:42',
    }]

    with app.app_context():
        borrowstate = BorrowState.query.get(1)
        assert borrowstate.returned_at == datetime.datetime(2020, 1, 6, 13, 37, 42)
