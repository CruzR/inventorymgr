"""Blueprint for the server-side views."""

from flask import Blueprint

views_blueprint = Blueprint(
    "views", "inventorymgr.views", static_folder="static", template_folder="templates"
)
