"""
Entry point for the web app, defines the flask application factory.

create_app()
    The flask application factory.
"""


import os
from typing import Any, Dict, Optional

from flask import Flask


def create_app(test_config: Optional[Dict[str, Any]] = None) -> Flask:
    """The Flask application factory."""

    # Lazy-loading of modules is intentional here.
    # pylint: disable=import-outside-toplevel
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'inventorymgr.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import api
    app.errorhandler(api.APIError)(api.handle_api_error)

    from . import users
    app.register_blueprint(users.bp)

    from . import db
    db.init_app(app)

    return app
