# -*- coding: utf-8 -*-

"""
Database connection for Cl4ptr4p project.

Using Flask 1.1.1

For more information on this file, see
README.md
"""
from .google_cloud import MYSQL_CLOUD, POSTGRESQL_CLOUD
from .custom_servers import MYSQL_CUSTOM, POSTGRESQL_CUSTOM
import os

# set the Database Connection
# "LOCAL", "CLOUD"
DATABASE_ENV = "LOCAL"

# set the Database Provider
# 'mysql', 'postgresql', 'nosql'
DATABASE_PROVIDER = 'mysql'


DATABASE_CONFIG = {
    'CLOUD': {
        'mysql': MYSQL_CLOUD,
        'postgresql': POSTGRESQL_CLOUD,
        'nosql': None
    },
    'LOCAL': {
        'mysql': MYSQL_CUSTOM,
        'postgresql': POSTGRESQL_CUSTOM,
        'nosql': None
    }
}

# set default Connection
DATABASE_CONNECTION = None

if os.environ.get('GAE_ENV', '').startswith('standard'):
    DATABASE_CONNECTION = DATABASE_CONFIG['CLOUD'][DATABASE_PROVIDER]
    print("DATABASE_CONNECTION CLOUD", DATABASE_CONNECTION)
else:
    DATABASE_CONNECTION = DATABASE_CONFIG['LOCAL'][DATABASE_PROVIDER]
    print("DATABASE_CONNECTION LOCAL", DATABASE_CONNECTION)
