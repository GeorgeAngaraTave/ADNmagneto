# -*- coding: utf-8 -*-

"""Python class to handle JSON responses."""

from flask import make_response, jsonify, Response
from app import api
from .cors import CORS_HEADERS


class Rest:
    @staticmethod
    @api.representation('application/json')
    def response(status_http=200, message='success', data=None, status_code=None, errors=None):
        data = None if data is None else data
        json_resp = {'status': status_code or status_http, 'message': message, 'data': data}
        if errors is not None:
            json_resp.update({'error': errors})
        resp = make_response(jsonify(json_resp), status_http)
        resp.headers.extend(CORS_HEADERS or {})
        return resp

    @staticmethod
    @api.representation('application/json')
    def response_custom(status_http=200, data=None):
        json_resp = {"message": "success"} if data is None else data
        resp = make_response(jsonify(json_resp), status_http)
        resp.headers.extend(CORS_HEADERS or {})
        return resp

    @staticmethod
    # @api.representation('application/xml')
    def response_xml(status_http=200, data=None):
        xml_resp = data if data is not None else "<root></root>"
        resp = make_response(xml_resp, status_http)
        resp.headers.extend(CORS_HEADERS or {})
        resp.headers.extend({'Content-Type': 'application/xml'} or {})
        return resp

    @staticmethod
    # @api.representation('application/csv')
    def response_csv(status_http=200, data=None, filename='exportCSV'):
        csv_resp = data if data is not None else "some;example\nplease;input data"
        resp = make_response(csv_resp, status_http)
        resp.headers.extend(CORS_HEADERS or {})
        resp.headers.extend({'Content-Type': 'application/csv'} or {})
        resp.headers.extend({'Content-Disposition': "attachment; filename={0}.csv".format(filename)} or {})
        return resp

    @staticmethod
    def raw_response(status_http=200, data=None):
        resp = Response(data, mimetype='text/html')
        return resp

    def response_tracking(status_http=200, message='success', data=None, status_code=None, errors=None):
        data = None if data is None else data
        if errors is None:
            resp = {
                'status': status_code or status_http,
                'message': message,
                'data': data
            }
        else:
            resp = {
                'status': status_code or status_http,
                'message': message,
                'errors': errors
            }
        return resp
