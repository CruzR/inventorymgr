import datetime

import pytest

from inventorymgr.db import db
from inventorymgr.db.models import (
    BorrowableItem,
    BorrowState,
    LogEntry,
    TransferRequest,
    User,
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
    assert response.json["transferrequests"][1] == {
        "id": 2,
        "borrowstate_id": 1,
        "target_user_id": 2,
    }


def test_accept_transfer_request_unauthenticated(client):
    response = client.delete("/api/v1/transferrequests/1", json={"action": "accept"})
    assert response.status_code == 403
    assert response.is_json
    assert response.json["reason"] == "authentication_required"


def test_accept_unknown_transfer_request(client, auth):
    auth.login("min_permissions_user")
    response = client.delete("/api/v1/transferrequests/3", json={"action": "accept"})
    assert response.status_code == 404
    assert response.is_json
    assert response.json["reason"] == "unknown_transfer_request"


def test_accept_transfer_request_for_other_user(client, auth):
    auth.login("test")
    response = client.delete("/api/v1/transferrequests/1", json={"action": "accept"})
    assert response.status_code == 403
    assert response.is_json
    assert response.json["reason"] == "insufficient_permissions"


def test_accept_transfer_request_with_missing_qualifications(client, auth, app):
    auth.login("min_permissions_user")
    response = client.delete("/api/v1/transferrequests/2", json={"action": "accept"})
    assert response.status_code == 403
    assert response.is_json
    assert response.json["reason"] == "missing_qualifications"


def test_cannot_accept_transfer_request_for_item_not_borrowed_by_issuer(
    client, auth, app
):
    with app.app_context():
        new_user = User(username="another_user", password="")
        tf = TransferRequest.query.get(1)
        bs = tf.borrowstate
        # Transfer borrowstate to another user to simulate item having changed hands
        new_user.borrowstates = [bs]
        db.session.add(new_user)
        db.session.commit()
        new_user_id = new_user.id
    auth.login("min_permissions_user")
    response = client.delete("/api/v1/transferrequests/1", json={"action": "accept"})
    assert response.status_code == 403
    assert response.is_json
    assert response.json["reason"] == "insufficient_permissions"
    with app.app_context():
        assert BorrowState.query.get(2).borrowing_user_id == new_user_id


def test_accept_transfer_request_successful(client, auth, app, monkeypatch):
    def fake_utcnow():
        return datetime.datetime(2020, 2, 7, 7, 53, 12)

    monkeypatch.setattr("inventorymgr.transfer_requests._utcnow", fake_utcnow)
    with app.app_context():
        transfer_request_count = TransferRequest.query.filter_by(
            target_user_id=2
        ).count()
        assert BorrowState.query.filter_by(borrowing_user_id=2).count() == 0
        assert LogEntry.query.filter_by(action="transfer").count() == 0

    auth.login("min_permissions_user")
    response = client.delete("/api/v1/transferrequests/1", json={"action": "accept"})
    assert response.status_code == 200
    assert response.is_json
    assert response.json["success"]

    with app.app_context():
        assert (
            TransferRequest.query.filter_by(target_user_id=2).count()
            == transfer_request_count - 1
        )
        borrowstate = BorrowState.query.filter_by(borrowing_user_id=2).one()
        assert borrowstate.borrowed_item_id == 3
        logentry = LogEntry.query.filter_by(action="transfer").one()
        assert logentry.timestamp == datetime.datetime(2020, 2, 7, 7, 53, 12)
        assert logentry.subject_id == 1
        assert logentry.items == [BorrowableItem.query.get(3)]
        assert logentry.secondary_id == 2


def test_decline_transfer_request_unauthenticated(client):
    response = client.delete("/api/v1/transferrequests/1", json={"action": "decline"})
    assert response.status_code == 403
    assert response.is_json
    assert response.json["reason"] == "authentication_required"


def test_decline_unknown_transfer_request(client, auth):
    auth.login("min_permissions_user")
    response = client.delete("/api/v1/transferrequests/3", json={"action": "decline"})
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
        transfer_request_count = TransferRequest.query.count()
        assert BorrowState.query.filter_by(borrowing_user_id=2).count() == 0
        assert LogEntry.query.filter_by(action="transfer").count() == 0

    auth.login("min_permissions_user")
    response = client.delete("/api/v1/transferrequests/1", json={"action": "decline"})
    assert response.status_code == 200
    assert response.is_json
    assert response.json["success"]

    with app.app_context():
        assert (
            TransferRequest.query.filter_by(target_user_id=2).count()
            == transfer_request_count - 1
        )
        assert BorrowState.query.filter_by(borrowing_user_id=2).count() == 0
        assert LogEntry.query.filter_by(action="transfer").count() == 0


def test_returning_item_deletes_transfer_request(client, auth, app):
    with app.app_context():
        transfer_request_count = TransferRequest.query.filter_by(
            target_user_id=2
        ).count()
    auth.login("test")
    response = client.post(
        "/api/v1/borrowstates/checkin", json={"user_id": 1, "item_ids": [1]}
    )
    assert response.status_code == 200
    with app.app_context():
        assert (
            TransferRequest.query.filter_by(target_user_id=2).count()
            == transfer_request_count - 1
        )


@pytest.fixture
def new_transfer_request_json():
    return {"target_user_id": 2, "borrowstate_id": 4}


@pytest.fixture
def new_transfer_request(new_transfer_request_json, app):
    with app.app_context():
        new_item = BorrowableItem(name="brand_new_item")
        db.session.add(new_item)
        db.session.add(
            BorrowState(
                borrowing_user_id=1,
                borrowed_item_id=2,
                received_at=datetime.datetime(2020, 2, 17, 6, 32),
                returned_at=datetime.datetime(2020, 2, 17, 6, 34),
            )
        )
        db.session.add(
            BorrowState(
                borrowing_user_id=1,
                borrowed_item=new_item,
                received_at=datetime.datetime(2020, 2, 17, 6, 32),
            )
        )
        db.session.commit()
    return new_transfer_request_json


def test_issue_transfer_request_unauthenticated(client, new_transfer_request):
    response = client.post("/api/v1/transferrequests", json=new_transfer_request)
    assert response.status_code == 403
    assert response.is_json
    assert response.json["reason"] == "authentication_required"


def test_issue_transfer_request_for_nonexistent_borrowstate(
    client, auth, new_transfer_request_json
):
    auth.login("test")
    response = client.post("/api/v1/transferrequests", json=new_transfer_request_json)
    assert response.status_code == 400
    assert response.is_json
    assert response.json["reason"] == "unknown_borrowstate"


def test_issue_transfer_request_for_returned_item(client, auth, new_transfer_request):
    auth.login("test")
    response = client.post(
        "/api/v1/transferrequests", json={"target_user_id": 2, "borrowstate_id": 3}
    )
    assert response.status_code == 400
    assert response.is_json
    assert response.json["reason"] == "item_not_borrowed"


def test_issue_transfer_request_for_other_user(client, auth, new_transfer_request):
    auth.login("min_permissions_user")
    response = client.post("/api/v1/transferrequests", json=new_transfer_request)
    assert response.status_code == 403
    assert response.is_json
    assert response.json["reason"] == "insufficient_permissions"


def test_issue_transfer_request_for_user_with_missing_qualifications(client, auth, app):
    # Clear previous illegal transfer request.
    with app.app_context():
        for transfer_request in TransferRequest.query.all():
            db.session.delete(transfer_request)
        db.session.commit()

    auth.login("test")
    # Try to re-create it via API request.
    response = client.post(
        "/api/v1/transferrequests", json={"target_user_id": 2, "borrowstate_id": 1}
    )
    # Should have failed because user is missing a qualification the item requires.
    assert response.status_code == 403
    assert response.is_json
    assert response.json["reason"] == "missing_qualifications"


def test_issue_transfer_request_successful(client, auth, new_transfer_request, app):
    with app.app_context():
        transfer_request_count = TransferRequest.query.filter_by(
            target_user_id=2
        ).count()
        assert (
            TransferRequest.query.filter_by(
                borrowstate_id=new_transfer_request["borrowstate_id"]
            ).count()
            == 0
        )

    auth.login("test")
    response = client.post("/api/v1/transferrequests", json=new_transfer_request)
    assert response.status_code == 200
    assert response.is_json
    assert response.json["success"]

    with app.app_context():
        assert (
            TransferRequest.query.filter_by(target_user_id=2).count()
            == transfer_request_count + 1
        )
        assert (
            TransferRequest.query.filter_by(
                borrowstate_id=new_transfer_request["borrowstate_id"]
            ).count()
            == 1
        )
