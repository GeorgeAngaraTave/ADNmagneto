# -*- coding: utf-8 -*-

"""
Database connection for Cl4ptr4p project.

Using Flask 1.1.1

For more information on this file, see
README.md
"""
import os


CUSTOM_SERVER = {
    'MYSQL': {
        'DB_HOST': os.environ.get('MYSQL_LOCAL_DB_HOST', '34.122.218.102'),
        'DB_USER': os.environ.get('MYSQL_LOCAL_DB_USER', 'useradmin'),
        'DB_PASSWD': os.environ.get('MYSQL_LOCAL_DB_PASSWD', '07h02xPDAaoA5pDd'),
        'DB_NAME': os.environ.get('MYSQL_LOCAL_DB_NAME', 'proyectos'),
        'DB_PORT': "3306"
    },
    'POSTGRESQL': {
        'DB_HOST': os.environ.get('POSTGRESQL_LOCAL_DB_HOST', 'localhost'),
        'DB_USER': os.environ.get('POSTGRESQL_LOCAL_DB_USER', 'postgres'),
        'DB_PASSWD': os.environ.get('POSTGRESQL_LOCAL_DB_PASSWD', 'postgres'),
        'DB_NAME': os.environ.get('POSTGRESQL_LOCAL_DB_NAME', 'postgres'),
        'DB_PORT': "5432"
    }
}
print('dbpass: ', CUSTOM_SERVER['MYSQL']['DB_PASSWD'])
# mysql+pymysql://<user>:<password>@<host>/<database>
if len(CUSTOM_SERVER['MYSQL']['DB_PASSWD']) > 0:
    MYSQL_CUSTOM = "mysql+pymysql://{0}:{1}@{2}/{3}".format(
        CUSTOM_SERVER['MYSQL']['DB_USER'],
        CUSTOM_SERVER['MYSQL']['DB_PASSWD'],
        CUSTOM_SERVER['MYSQL']['DB_HOST'],
        CUSTOM_SERVER['MYSQL']['DB_NAME']
    )
else:
    # mysql+pymysql://<user>@<host>/<database>
    MYSQL_CUSTOM = "mysql+pymysql://{0}@{1}/{2}".format(
        CUSTOM_SERVER['MYSQL']['DB_USER'],
        CUSTOM_SERVER['MYSQL']['DB_HOST'],
        CUSTOM_SERVER['MYSQL']['DB_NAME']
    )

# local_postgresql = "postgresql+psycopg2://<user>:<password>@<host>:<port>/<database>"
POSTGRESQL_CUSTOM = "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
    CUSTOM_SERVER['POSTGRESQL']['DB_USER'],
    CUSTOM_SERVER['POSTGRESQL']['DB_PASSWD'],
    CUSTOM_SERVER['POSTGRESQL']['DB_HOST'],
    CUSTOM_SERVER['POSTGRESQL']['DB_PORT'],
    CUSTOM_SERVER['POSTGRESQL']['DB_NAME']
)
