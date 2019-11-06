from inventorymgr import create_app


def test_factory_works():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
