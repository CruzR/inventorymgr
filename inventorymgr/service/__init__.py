"""
Shared business logic.

This package contains business logic shared by JSON API endpoints
and HTML endpoints.
"""

from inventorymgr.service.users import *

__all__ = ["create_user", "update_user", "delete_user"]
