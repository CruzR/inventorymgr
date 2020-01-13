from inventorymgr.db.models import BorrowableItem, User


def test_create_item_unauthenticated(client):
    response = client.post('/api/v1/items', json={
        'name': 'new_item',
        'required_qualifications': [{'id': 1, 'name': "Driver's License"}]
    })
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'


def test_create_item_insufficient_permissions(client, auth):
    auth.login('min_permissions_user')
    response = client.post('/api/v1/items', json={
        'name': 'new_item',
        'required_qualifications': [{'id': 1, 'name': "Driver's License"}]
    })
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'insufficient_permissions'


def test_create_existing_item(client, auth):
    auth.login('test')
    response = client.post('/api/v1/items', json={
        'name': 'existing_item',
        'required_qualifications': [{'id': 1, 'name': "Driver's License"}]
    })
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'item_exists'


def test_create_item_unknown_qualification(client, auth):
    auth.login('test')
    response = client.post('/api/v1/items', json={
        'name': 'new_item',
        'required_qualifications': [{'id': 2, 'name': 'other_qualification'}],
    })
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'unknown_qualification'


def test_create_item_success(client, auth, app):
    auth.login('test')
    response = client.post('/api/v1/items', json={
        'name': 'new_item',
        'required_qualifications': [{'id': 1, 'name': "Driver's License"}]
    })
    assert response.status_code == 200
    assert response.is_json
    assert response.json['id'] == 3
    assert response.json['name'] == 'new_item'
    assert response.json['barcode'] == '0000000000003'
    assert response.json['required_qualifications'] == [{'id': 1, 'name': "Driver's License"}]

    with app.app_context():
        assert BorrowableItem.query.count() == 3
        item = BorrowableItem.query.get(3)
        assert item.name == 'new_item'
        assert item.required_qualifications[0].id == 1
        assert item.required_qualifications[0].name == "Driver's License"


def test_list_items_unauthenticated(client):
    response = client.get('/api/v1/items')
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'


def test_list_items_success(client, auth):
    auth.login('min_permissions_user')
    response = client.get('/api/v1/items')
    assert response.status_code == 200
    assert response.is_json
    assert response.json['items'] == [
        {'id': 1,
         'name': 'existing_item',
         'barcode': '0000000000001',
         'required_qualifications': [{'id': 1, 'name': "Driver's License"}]},
        {'id': 2,
         'name': 'another_item',
         'barcode': '0000000000002',
         'required_qualifications': [{'id': 1, 'name': "Driver's License"}]}]


def test_update_item_unauthenticated(client):
    response = client.put('/api/v1/items/1',
        json={'id': 1, 'name': 'new_item_name', 'required_qualifications': []})
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'


def test_update_item_insufficient_permissions(client, auth):
    auth.login('min_permissions_user')
    response = client.put('/api/v1/items/1',
        json={'id': 1, 'name': 'new_item_name', 'required_qualifications': []})
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'insufficient_permissions'


def test_update_item_id_mismatch(client, auth):
    auth.login('test')
    response = client.put('/api/v1/items/1',
        json={'id': 2, 'name': 'new_item_name', 'required_qualifications': []})
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'id_mismatch'


def test_update_item_nonexistent_item(client, auth):
    auth.login('test')
    response = client.put('/api/v1/items/3',
        json={'id': 3, 'name': 'new_item_name', 'required_qualifications': []})
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'nonexistent_item'


def test_update_item_success(client, auth, app):
    auth.login('test')
    response = client.put('/api/v1/items/1',
        json={'id': 1, 'name': 'new_item_name', 'required_qualifications': []})
    assert response.status_code == 200
    assert response.is_json
    assert response.json['id'] == 1
    assert response.json['name'] == 'new_item_name'
    assert response.json['barcode'] == '0000000000001'
    assert response.json['required_qualifications'] == []

    with app.app_context():
        assert BorrowableItem.query.count() == 2
        assert BorrowableItem.query.filter_by(name='new_item_name').count() == 1


def test_delete_item_unauthenticated(client):
    response = client.delete('/api/v1/items/1');
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'


def test_delete_item_insufficient_permissions(client, auth):
    auth.login('min_permissions_user')
    response = client.delete('/api/v1/items/1')
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'insufficient_permissions'


def test_delete_nonexistent_item(client, auth):
    auth.login('test')
    response = client.delete('/api/v1/items/42')
    assert response.status_code == 200
    assert response.is_json
    assert response.json['success']


def test_delete_item_success(client, auth, app):
    auth.login('test')
    response = client.delete('/api/v1/items/1')
    assert response.status_code == 200
    assert response.is_json
    assert response.json['success']

    with app.app_context():
        assert BorrowableItem.query.filter_by(name='existing_item').count() == 0
