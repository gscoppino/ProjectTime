from .settings import *

DEBUG = True

DEBUG_TOOLBAR_CONFIG = {'SHOW_TOOLBAR_CALLBACK': lambda _: DEBUG}

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

INSTALLED_APPS.extend([
    'debug_toolbar'
])
