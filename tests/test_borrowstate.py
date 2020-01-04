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
