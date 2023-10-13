#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from time import strftime

from flask import request

from app import flask_app

from app.config.local_settings import DEBUG, DEFAULT_HOST, DEFAULT_PORT
from app.ext.rest import HttpStatus, Rest


@flask_app.route('/')
def home():
    return Rest.response(200, HttpStatus.OK, {'home': 'welcome to BackEndBase, use /api instead'})


@flask_app.errorhandler(404)
def not_found(error):
    return Rest.response(404, 'not found')


@flask_app.errorhandler(413)
def request_entity_too_large(error):
    return Rest.response(413, 'The file is too large')


@flask_app.errorhandler(500)
def internal_error(error):
    logging.exception('An error occurred during a request.')
    return Rest.response(500, None, [])


@flask_app.after_request
def after_request(response):
    """ Logging after every request. """
    # This avoids the duplication of registry in the log,
    # since that 500 is already logged via @app.errorhandler.
    logging.info("after_request")
    if response.status_code != 500:
        ts = strftime('[%Y-%b-%d %H:%M]')
        print("ts::{} ra::{} me::{} sc::{} fp::{} st::{} url::{} ct::{} ua::{} au::{}".format(
            ts,
            request.remote_addr,
            request.method,
            request.scheme,
            request.full_path,
            response.status,
            request.url,
            request.content_type,
            request.user_agent,
            request.headers.get('Authorization', 'without_headers'),
        ))
    return response

# better gunicorn logger
# gunicorn_logger = logging.getLogger('gunicorn.error')
# app.logger.handlers = gunicorn_logger.handlers
# app.logger.setLevel(gunicorn_logger.level)

if __name__ == '__main__':
    print('running python server from main')
    #flask_app.run(host=DEFAULT_HOST, port=DEFAULT_PORT, debug=DEBUG)
    flask_app.run(host=DEFAULT_HOST, port=DEFAULT_PORT, debug=DEBUG)
