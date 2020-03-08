TEMPLATES_AUTO_RELOAD = True
EXPLAIN_TEMPLATE_LOADING = True
# FLASK_DEBUG = True
# env = 'development'

import os
db_path = os.path.join(os.path.dirname(__file__), 'bakery.db')

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICAIONS = False

from tempfile import mkdtemp
from datetime import timedelta
SESSION_FILE_DIR=mkdtemp()
SESSION_PERMANENT=True
PERMANENT_SESSION_LIFETIME = timedelta(minutes = 30)
SESSION_REFRESH_EACH_REQUEST = True
# SEND_FILE_MAX_AGE_DEFAULT = timedelta(minutes = 1)
SESSION_TYPE='filesystem'
REMEMBER_COOKIE_DURAITON = timedelta(minutes = 30)

import secrets

# SECRET_KEY = secrets.token_hex(16)

UPLOAD_FOLDER = "static/images/uploads"

LOG_TO_STDOUT = 1
