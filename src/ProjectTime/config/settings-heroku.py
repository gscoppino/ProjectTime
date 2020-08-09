import django_heroku
from .settings import *

DEBUG = False
django_heroku.settings(locals())
