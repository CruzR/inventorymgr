"""Server-side views for inventorymgr."""


import inventorymgr.views.auth
from inventorymgr.views.blueprint import views_blueprint


__all__ = ["views_blueprint"]
