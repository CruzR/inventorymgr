from inventorymgr.db.models import Qualification


def test_list_qualifications_unauthenticated(client):
    response = client.get('http://localhost:5000/api/v1/qualifications')
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'


def test_list_qualifications(client):
    client.post(
        'http://localhost:5000/auth/login',
        json={'username': 'min_permissions_user', 'password': 'test'}
    )
    response = client.get('http://localhost:5000/api/v1/qualifications')
    assert response.status_code == 200
    assert response.is_json
    assert response.json == [{'id': 1, 'name': "Driver's License"}]


def test_create_qualification_unauthenticated(client, app):
    response = client.post(
        'http://localhost:5000/api/v1/qualifications', json={'name': 'test'})
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'

    with app.app_context():
        assert Qualification.query.filter_by(name='test').count() == 0


def test_create_qualification_with_insufficient_permissions(client, app):
    client.post(
        'http://localhost:5000/auth/login',
        json={'username': 'min_permissions_user', 'password': 'test'}
    )
    response = client.post(
        'http://localhost:5000/api/v1/qualifications', json={'name': 'test'})
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'insufficient_permissions'

    with app.app_context():
        assert Qualification.query.filter_by(name='test').count() == 0


def test_create_qualification(client, app):
    client.post(
        'http://localhost:5000/auth/login',
        json={'username': 'test', 'password': 'test'}
    )
    response = client.post(
        'http://localhost:5000/api/v1/qualifications', json={'name': 'test'})
    assert response.status_code == 200
    assert response.is_json
    assert response.json == {'id': 2, 'name': 'test'}
    with app.app_context():
        assert Qualification.query.filter_by(name='test').count() == 1
        assert Qualification.query.filter_by(name="Driver's License").count() == 1


def test_create_qualification_with_id_set(client, app):
    client.post(
        'http://localhost:5000/auth/login',
        json={'username': 'test', 'password': 'test'}
    )
    response = client.post(
        'http://localhost:5000/api/v1/qualifications', json={'name': 'test', 'id': 1})
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'id_specified'
    with app.app_context():
        assert Qualification.query.filter_by(name='test').count() == 0


def test_create_qualification_with_existing_object(client, app):
    client.post(
        'http://localhost:5000/auth/login',
        json={'username': 'test', 'password': 'test'}
    )
    response = client.post(
        'http://localhost:5000/api/v1/qualifications', json={'name': "Driver's License"})
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'object_exists'
    with app.app_context():
        assert Qualification.query.filter_by(name="Driver's License").count() == 1


def test_update_qualification_unauthenticated(client, app):
    response = client.put(
        'http://localhost:5000/api/v1/qualifications/1',
        json={'id': 1, 'name': 'test'})
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'
    with app.app_context():
        assert Qualification.query.filter_by(name='test').count() == 0
        assert Qualification.query.filter_by(name="Driver's License").count() == 1


def test_update_qualification_with_insufficient_permissions(client, app):
    client.post(
        'http://localhost:5000/auth/login',
        json={'username': 'min_permissions_user', 'password': 'test'}
    )
    response = client.put(
        'http://localhost:5000/api/v1/qualifications/1',
        json={'id': 1, 'name': 'test'})
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'insufficient_permissions'
    with app.app_context():
        assert Qualification.query.filter_by(name='test').count() == 0
        assert Qualification.query.filter_by(name="Driver's License").count() == 1


def test_update_qualification_with_incorrect_id(client, app):
    client.post(
        'http://localhost:5000/auth/login',
        json={'username': 'test', 'password': 'test'}
    )
    response = client.put(
        'http://localhost:5000/api/v1/qualifications/1',
        json={'id': 2, 'name': 'test'})
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'incorrect_id'
    with app.app_context():
        assert Qualification.query.filter_by(name='test').count() == 0
        assert Qualification.query.filter_by(name="Driver's License").count() == 1


def test_update_qualification_with_nonexistant_object(client, app):
    client.post(
        'http://localhost:5000/auth/login',
        json={'username': 'test', 'password': 'test'}
    )
    response = client.put(
        'http://localhost:5000/api/v1/qualifications/2',
        json={'id': 2, 'name': 'test'})
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'no_such_object'
    with app.app_context():
        assert Qualification.query.filter_by(name='test').count() == 0
        assert Qualification.query.filter_by(name="Driver's License").count() == 1


def test_update_qualification(client, app):
    client.post(
        'http://localhost:5000/auth/login',
        json={'username': 'test', 'password': 'test'}
    )
    response = client.put(
        'http://localhost:5000/api/v1/qualifications/1',
        json={'id': 1, 'name': 'test'})
    assert response.status_code == 200
    assert response.is_json
    assert response.json == {'id': 1, 'name': 'test'}
    with app.app_context():
        assert Qualification.query.filter_by(name="Driver's License").count() == 0
        assert Qualification.query.filter_by(name='test').count() == 1


def test_delete_qualification_unauthenticated(client, app):
    response = client.delete(
        'http://localhost:5000/api/v1/qualifications/1',
        json={'id': 1, 'name': "Driver's License"})
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'authentication_required'
    with app.app_context():
        assert Qualification.query.filter_by(name="Driver's License").count() == 1


def test_delete_qualification_with_insufficient_permissions(client, app):
    client.post(
        'http://localhost:5000/auth/login',
        json={'username': 'min_permissions_user', 'password': 'test'}
    )
    response = client.delete(
        'http://localhost:5000/api/v1/qualifications/1',
        json={'id': 1, 'name': "Driver's License"})
    assert response.status_code == 403
    assert response.is_json
    assert response.json['reason'] == 'insufficient_permissions'
    with app.app_context():
        assert Qualification.query.filter_by(name="Driver's License").count() == 1


def test_delete_qualification_with_incorrect_id(client, app):
    client.post(
        'http://localhost:5000/auth/login',
        json={'username': 'test', 'password': 'test'}
    )
    response = client.delete(
        'http://localhost:5000/api/v1/qualifications/1',
        json={'id': 2, 'name': 'test'})
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'incorrect_id'
    with app.app_context():
        assert Qualification.query.filter_by(name="Driver's License").count() == 1


def test_delete_qualification_with_nonexistant_object(client, app):
    client.post(
        'http://localhost:5000/auth/login',
        json={'username': 'test', 'password': 'test'}
    )
    response = client.delete(
        'http://localhost:5000/api/v1/qualifications/2',
        json={'id': 2, 'name': 'test'})
    assert response.status_code == 400
    assert response.is_json
    assert response.json['reason'] == 'no_such_object'
    with app.app_context():
        assert Qualification.query.filter_by(name="Driver's License").count() == 1


def test_delete_qualification(client, app):
    client.post(
        'http://localhost:5000/auth/login',
        json={'username': 'test', 'password': 'test'}
    )
    response = client.delete(
        'http://localhost:5000/api/v1/qualifications/1',
        json={'id': 1, 'name': 'test'})
    assert response.status_code == 200
    assert response.is_json
    assert response.json == {'success': True}
    with app.app_context():
        assert Qualification.query.filter_by(name="Driver's License").count() == 0
