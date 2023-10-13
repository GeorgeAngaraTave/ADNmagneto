# -*- coding: utf-8 -*-

import sys
import logging
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS

from .config.databases.settings import DATABASE_CONNECTION
from .config.local_settings import ALLOW_METHODS, USE_STDERR
from .config.local_settings import DEFAULT_CACHE
from .config.storage import MAX_FILE_SIZE, DEFAULT_BUCKET
from .config.settings import SECRET_KEY
from .config.cache import init_cache
from flask_caching import Cache



SDK_ENV = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', None)

class FatalError(Exception):
    """FatalError shouldn't be retried."""
    pass

if not SDK_ENV:
    print()
    print("Could not automatically determine credentials.")
    print("Please set GOOGLE_APPLICATION_CREDENTIALS or explicitly create credentials and re-run the application.")
    print("For more information, please see https://cloud.google.com/docs/authentication/getting-started")
    print()

app = Flask(__name__)
#flask_app = Flask(__name__)
flask_app = app

# Settings for Storgae
app.config.update(dict(
    SECRET_KEY=SECRET_KEY,
    MAX_CONTENT_LENGTH=MAX_FILE_SIZE,
    UPLOAD_FOLDER=DEFAULT_BUCKET,
))

# Settings for Cache
cache = None

if DEFAULT_CACHE is not None:
    config_cache = init_cache(DEFAULT_CACHE)
    cache = Cache(app, config=config_cache)

# Settings for DB
db = None

if DATABASE_CONNECTION is not None:
    SQLALCHEMY_DATABASE_URI = DATABASE_CONNECTION

    app.config.update(dict(
        SQLALCHEMY_ECHO=False,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI,
    ))
    db = SQLAlchemy(app)

api = Api(app)

# from .controllers import api_spatial

# flask_app.register_blueprint(api_spatial)

# cors = CORS(flask_app, resources={r"/api/*": {"allow_headers": "*", "supports_credentials": "true", "max_age": 1, "methods": ALLOW_METHODS}})
cors = CORS(app, resources={r"/api/*": {"allow_headers": "*", "supports_credentials": "true", "max_age": 1, "methods": ALLOW_METHODS}})

#register modules
from app.ext.register import Register
reg_api = Register()

if USE_STDERR:
    logging.basicConfig(stream=sys.stderr)
