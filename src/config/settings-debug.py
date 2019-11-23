from .settings import *

DEBUG = True

DEBUG_TOOLBAR_PATCH_SETTINGS = False

INTERNAL_IPS = ['127.0.0.1']

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

INSTALLED_APPS.extend([
    'debug_toolbar'
])
