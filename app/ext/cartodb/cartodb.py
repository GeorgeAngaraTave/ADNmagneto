# -*- coding: utf-8 -*-

"""Python module for CartoDB."""

# CartoDB SQL API v2
# https://carto.com/developers/sql-api/
# Interact with your tables and data inside CARTO, as if you were running SQL statements.


from app.ext.rest import consumer
from app.config.cartodb import CARTODB_URI, CARTODB_ACCOUNT, CARTODB_API_KEY
import logging as log


carto_api_config = {
    'uri': CARTODB_URI.format(CARTODB_ACCOUNT),
    'key': CARTODB_API_KEY,
}


def sql_api(sql=None):
    if sql is None:
        return None

    params = {
        'api_key': carto_api_config['key'],
        'q': sql
    }

    resp = consumer(carto_api_config['uri'], 'POST', params, use_ssl=True)

    if resp is None:
        log.info("cartodb result none")
        return None
    else:
        if 'rows' in resp:
            log.info("cartodb result success")
            return resp
        elif 'error' in resp:
            log.warning("cartodb result error")
            return resp

def create_job(sql=None):
    if sql is None:
        return None

    params = {
        'api_key': carto_api_config['key'],
        'query': sql
    }

    uri = "{0}/{1}".format(carto_api_config['uri'], 'job')
    resp = consumer(uri, 'POST', params, use_ssl=True)

    if resp is None:
        log.info("cartodb result job none")
        return None
    else:
        if 'job_id' in resp:
            log.info("cartodb result job success")
            return resp
        elif 'error' in resp:
            log.warning("cartodb result job error")
            return resp

def get_job(job_id=None):
    if job_id is None:
        return None

    # example
    # https://awesome_cartodb_account.cartodb.com/api/v2/sql/job/JOB_ID?api_key=awesome_cartodb_api_key

    uri = "{0}/{1}/{2}?api_key={3}".format(carto_api_config['uri'], 'job', job_id, carto_api_config['key'])
    resp = consumer(uri, 'GET', use_ssl=True)

    if resp is None:
        log.info("cartodb result get job none")
        return None
    else:
        if 'status' in resp:
            log.info("cartodb result get job success")
            return resp
        elif 'error' in resp:
            log.warning("cartodb result get job error")
            return resp
