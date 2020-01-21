from inventorymgr.db import db


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db(self):
        Recorder.called = True

    monkeypatch.setattr(
        "inventorymgr.db.db.create_all", fake_init_db.__get__(db, type(db))
    )
    result = runner.invoke(args=["init-db"])
    assert "Initialized" in result.output
    assert Recorder.called
