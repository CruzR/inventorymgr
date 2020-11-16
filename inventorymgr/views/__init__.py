"""Server-side views for inventorymgr."""


import inventorymgr.views.auth
import inventorymgr.views.borrowstates
import inventorymgr.views.dashboard
import inventorymgr.views.items
import inventorymgr.views.qualifications
import inventorymgr.views.registration
import inventorymgr.views.users
from inventorymgr.views.blueprint import views_blueprint


__all__ = ["views_blueprint"]
