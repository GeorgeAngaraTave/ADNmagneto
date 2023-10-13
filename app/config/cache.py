# -*- coding: utf-8 -*-

# Cache Settings
# For more information on this file, see README.md

from app.config.local_settings import SESSION_EXPIRE_TIME

def init_cache(cache):

    if cache == 'filesystem':
        config = {
            'CACHE_TYPE': 'filesystem',
            'CACHE_DIR': '/tmp',
            'CACHE_DEFAULT_TIMEOUT': SESSION_EXPIRE_TIME,
        }
        return config

    if cache == 'memcached':
        config = {
            'CACHE_TYPE': 'memcached',
            'CACHE_DEFAULT_TIMEOUT': SESSION_EXPIRE_TIME,
        }
        return config

    if cache == 'simple':
        config = {
            'CACHE_TYPE': 'simple',
            'CACHE_DEFAULT_TIMEOUT': SESSION_EXPIRE_TIME,
            'CACHE_IGNORE_ERRORS': True,
            'CACHE_THRESHOLD': 500,
        }
        return config

    return None
