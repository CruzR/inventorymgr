from inventorymgr.db.models import BorrowableItem, User


def test_create_item_unauthenticated(client):
    response = client.post('/api/v1/items', json={'name': 'new_item'})
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'


def test_create_item_insufficient_permissions(client, auth):
    auth.login('min_permissions_user')
    response = client.post('/api/v1/items', json={'name': 'new_item'})
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'insufficient_permissions'


def test_create_existing_item(client, auth):
    auth.login('test')
    response = client.post('/api/v1/items', json={'name': 'existing_item'})
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'item_exists'


def test_create_item_success(client, auth, app):
    auth.login('test')
    response = client.post('/api/v1/items', json={'name': 'new_item'})
    assert response.status_code == 200
    assert response.is_json
    assert response.json['id'] == 2
    assert response.json['name'] == 'new_item'
    assert response.json['barcode'] == '0000000000002'

    with app.app_context():
        assert BorrowableItem.query.count() == 2
        item = BorrowableItem.query.get(2)
        assert item.name == 'new_item'


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
        {'id': 1, 'name': 'existing_item', 'barcode': '0000000000001'}]


def test_update_item_unauthenticated(client):
    response = client.put('/api/v1/items/1', json={'id': 1, 'name': 'new_item_name'})
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'


def test_update_item_insufficient_permissions(client, auth):
    auth.login('min_permissions_user')
    response = client.put('/api/v1/items/1', json={'id': 1, 'name': 'new_item_name'})
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'insufficient_permissions'


def test_update_item_id_mismatch(client, auth):
    auth.login('test')
    response = client.put('/api/v1/items/1', json={'id': 2, 'name': 'new_item_name'})
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'id_mismatch'


def test_update_item_nonexistent_item(client, auth):
    auth.login('test')
    response = client.put('/api/v1/items/2', json={'id': 2, 'name': 'new_item_name'})
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'nonexistent_item'


def test_update_item_success(client, auth, app):
    auth.login('test')
    response = client.put('/api/v1/items/1', json={'id': 1, 'name': 'new_item_name'})
    assert response.status_code == 200
    assert response.is_json
    assert response.json['id'] == 1
    assert response.json['name'] == 'new_item_name'
    assert response.json['barcode'] == '0000000000001'

    with app.app_context():
        assert BorrowableItem.query.count() == 1
        assert BorrowableItem.query.filter_by(name='new_item_name').count() == 1
