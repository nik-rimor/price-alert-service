import os

DEBUG = True
ADMINS = frozenset([os.getenv('APP_ADMIN')])
APP_SECRET_KEY = os.getenv('APP_SECRET_KEY')

