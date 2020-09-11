"""Server-side views for inventorymgr."""


import inventorymgr.views.auth
import inventorymgr.views.registration
from inventorymgr.views.blueprint import views_blueprint


__all__ = ["views_blueprint"]
