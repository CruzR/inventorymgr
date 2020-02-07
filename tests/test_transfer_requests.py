import datetime

from inventorymgr.db.models import (
    BorrowableItem,
    BorrowState,
    LogEntry,
    TransferRequest,
)


def test_get_transfer_requests_unauthenticated(client):
    response = client.get("/api/v1/transferrequests")
    assert response.status_code == 403
    assert response.is_json
    assert response.json["reason"] == "authentication_required"


def test_get_transfer_requests_success(client, auth):
    auth.login("min_permissions_user")
    response = client.get("/api/v1/transferrequests")
    assert response.status_code == 200
    assert response.is_json
    assert response.json["transferrequests"] == [{"id": 1, "borrowstate_id": 1}]


def test_accept_transfer_request_unauthenticated(client):
    response = client.delete("/api/v1/transferrequests/1", json={"action": "accept"})
    assert response.status_code == 403
    assert response.is_json
    assert response.json["reason"] == "authentication_required"


def test_accept_unknown_transfer_request(client, auth):
    auth.login("min_permissions_user")
    response = client.delete("/api/v1/transferrequests/2", json={"action": "accept"})
    assert response.status_code == 404
    assert response.is_json
    assert response.json["reason"] == "unknown_transfer_request"


def test_accept_transfer_request_for_other_user(client, auth):
    auth.login("test")
    response = client.delete("/api/v1/transferrequests/1", json={"action": "accept"})
    assert response.status_code == 403
    assert response.is_json
    assert response.json["reason"] == "insufficient_permissions"


def test_accept_transfer_request_successful(client, auth, app, monkeypatch):
    def fake_utcnow():
        return datetime.datetime(2020, 2, 7, 7, 53, 12)

    monkeypatch.setattr("inventorymgr.transfer_requests._utcnow", fake_utcnow)
    with app.app_context():
        assert BorrowState.query.filter_by(borrowing_user_id=2).count() == 0
        assert LogEntry.query.filter_by(action="transfer").count() == 0

    auth.login("min_permissions_user")
    response = client.delete("/api/v1/transferrequests/1", json={"action": "accept"})
    assert response.status_code == 200
    assert response.is_json
    assert response.json["success"]

    with app.app_context():
        assert TransferRequest.query.filter_by(target_user_id=2).count() == 0
        borrowstate = BorrowState.query.filter_by(borrowing_user_id=2).one()
        assert borrowstate.borrowed_item_id == 1
        logentry = LogEntry.query.filter_by(action="transfer").one()
        assert logentry.timestamp == datetime.datetime(2020, 2, 7, 7, 53, 12)
        assert logentry.subject_id == 1
        assert logentry.items == [BorrowableItem.query.get(1)]
        assert logentry.secondary_id == 2


def test_decline_transfer_request_unauthenticated(client):
    response = client.delete("/api/v1/transferrequests/1", json={"action": "decline"})
    assert response.status_code == 403
    assert response.is_json
    assert response.json["reason"] == "authentication_required"


def test_decline_unknown_transfer_request(client, auth):
    auth.login("min_permissions_user")
    response = client.delete("/api/v1/transferrequests/2", json={"action": "decline"})
    assert response.status_code == 404
    assert response.is_json
    assert response.json["reason"] == "unknown_transfer_request"


def test_decline_transfer_request_for_other_user(client, auth):
    auth.login("test")
    response = client.delete("/api/v1/transferrequests/1", json={"action": "decline"})
    assert response.status_code == 403
    assert response.is_json
    assert response.json["reason"] == "insufficient_permissions"


def test_decline_transfer_request_successful(client, auth, app):
    with app.app_context():
        assert BorrowState.query.filter_by(borrowing_user_id=2).count() == 0
        assert LogEntry.query.filter_by(action="transfer").count() == 0

    auth.login("min_permissions_user")
    response = client.delete("/api/v1/transferrequests/1", json={"action": "decline"})
    assert response.status_code == 200
    assert response.is_json
    assert response.json["success"]

    with app.app_context():
        assert TransferRequest.query.filter_by(target_user_id=2).count() == 0
        assert BorrowState.query.filter_by(borrowing_user_id=2).count() == 0
        assert LogEntry.query.filter_by(action="transfer").count() == 0


def test_returning_item_deletes_transfer_request(client, auth, app):
    auth.login("test")
    response = client.post(
        "/api/v1/borrowstates/checkin", json={"user_id": 1, "item_ids": [1]}
    )
    assert response.status_code == 200
    with app.app_context():
        assert TransferRequest.query.filter_by(target_user_id=2).count() == 0
