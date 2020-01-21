"""
Entry point for the web app, defines the flask application factory.

create_app()
    The flask application factory.
"""


import os
from typing import Any, Dict, Optional

from flask import Flask
from sqlalchemy import event  # type: ignore


def create_app(test_config: Optional[Dict[str, Any]] = None) -> Flask:
    """The Flask application factory."""

    # Lazy-loading of modules is intentional here.
    # pylint: disable=import-outside-toplevel
    app = Flask(__name__, instance_relative_config=True)

    db_path = os.path.join(app.instance_path, "inventorymgr.sqlite")

    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///{}".format(db_path),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SERVER_NAME="localhost:5000",
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import api

    app.errorhandler(api.APIError)(api.handle_api_error)
    app.register_blueprint(api.bp)

    from . import auth

    app.register_blueprint(auth.bp)

    from . import registration

    app.register_blueprint(registration.bp)
    app.cli.add_command(registration.generate_registration_token_command)

    from . import qualifications

    app.register_blueprint(qualifications.bp)

    from . import users

    app.register_blueprint(users.bp)
    app.cli.add_command(users.create_user_command)

    from .db import db, init_db_command

    db.init_app(app)
    app.cli.add_command(init_db_command)

    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite:"):

        def _sqlite_enforce_foreign_keys(dbapi_con: Any, _con_record: Any) -> None:
            dbapi_con.execute("PRAGMA foreign_keys=ON;")

        with app.app_context():  # type: ignore
            event.listen(db.engine, "connect", _sqlite_enforce_foreign_keys)

    from .app import bp

    app.register_blueprint(bp)

    from . import items

    app.register_blueprint(items.bp)

    from . import borrowstates

    app.register_blueprint(borrowstates.bp)

    from . import error_reports

    app.register_blueprint(error_reports.bp)

    return app
