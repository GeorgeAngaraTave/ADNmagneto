#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from app import app as Application
from app.config.local_settings import DEFAULT_HOST, DEFAULT_PORT, DEBUG
from app.ext.rest import Rest


@Application.errorhandler(404)
def not_found(error):
    return Rest.response(404, 'not found')


@Application.errorhandler(413)
def request_entity_too_large(error):
    return Rest.response(413, 'The file is too large')


@Application.errorhandler(500)
def internal_error(error):
    logging.exception('An error occurred during a request.')
    return Rest.response(500, None, [])


if __name__ == '__main__':
    print('running app python server from main/wsgi')
    # using uwsgi
    Application.run(host=DEFAULT_HOST, debug=DEBUG)
    # Application.run(host=DEFAULT_HOST, port=DEFAULT_PORT, debug=DEBUG)
