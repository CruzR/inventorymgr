"""Javascript error reporting API endpoints."""

import datetime

from flask import Blueprint, request

from inventorymgr.db import db
from inventorymgr.db.models import JavascriptError

bp = Blueprint("errorreports", __name__, url_prefix="/api/v1/errors")


@bp.route("/js", methods=("POST",))
def javascript_error() -> str:
    """API endpoint to store a JS error report."""
    if request.is_json:
        platform = request.user_agent.platform
        browser = request.user_agent.browser
        browser_version = request.user_agent.version
        browser_language = request.user_agent.language
        row = {
            "timestamp": datetime.datetime.utcnow(),
            "user_agent_raw": request.user_agent.string,
            "platform": platform,
            "browser": browser,
            "browser_version": browser_version,
            "browser_language": browser_language,
            "location": request.json["location"],
            "message": request.json.get("message"),
            "source": request.json.get("source"),
            "lineno": request.json.get("lineno"),
            "colno": request.json.get("colno"),
            "stack": request.json.get("stack"),
        }
        db.session.add(JavascriptError(**row))
        db.session.commit()
    return ""
