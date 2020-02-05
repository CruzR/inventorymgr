from inventorymgr.db import db
from inventorymgr.db.models import BorrowableItem, LogEntry, User


def test_get_logs_unathenticated(client):
    response = client.get("/api/v1/logs")
    assert response.status_code == 403
    assert response.is_json
    assert response.json["reason"] == "authentication_required"


def test_get_logs(client, auth):
    auth.login("min_permissions_user")
    response = client.get("/api/v1/logs")
    assert response.status_code == 200
    assert response.is_json
    assert response.json["logs"] == [
        {
            "id": 1,
            "timestamp": "2020-01-02T12:34:56",
            "action": "checkout",
            "subject_id": 1,
            "items": [{"id": 1, "barcode": "0000000000001"}],
        }
    ]


def test_delete_user_deletes_logs(app):
    with app.app_context():
        assert LogEntry.query.count() == 1
        db.session.delete(User.query.get(1))
        db.session.commit()
        assert LogEntry.query.count() == 0
