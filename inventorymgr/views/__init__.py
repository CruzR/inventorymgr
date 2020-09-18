"""Server-side views for inventorymgr."""


import inventorymgr.views.auth
import inventorymgr.views.registration
import inventorymgr.views.users
from inventorymgr.views.blueprint import views_blueprint


__all__ = ["views_blueprint"]
