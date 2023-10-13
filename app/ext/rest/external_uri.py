# -*- coding: utf-8 -*-

"""Python module for consuming external urls using urllib."""

import urllib
import urllib.request
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

import ssl as ssl_lib
import json
import xml.etree.ElementTree as xmlTree
import logging as log


class StoreCookie(object):
    the_cookie = None

    @classmethod
    def save_cookie(self, new_cookie):
        self.the_cookie = new_cookie

    def get_cookie(self):
        return self.the_cookie

    def remove_cookie(self):
        self.the_cookie = None


cookie_jar = StoreCookie()


def consumer(uri=None, method='GET', data=None, custom_headers=None, session=False, use_ssl=False, options=None):
    if uri is None:
        return None

    _default_header = {'Content-Type': 'application/json'}
    _url = uri
    _data = None if data is None else json.dumps(data)
    _method = 'GET' if method is None else method
    _req = None
    _default_timeout = 60

    if options is not None:
        if options == 'xml':
            _default_header = custom_headers
            _data = None if data is None else str(data)
        else:
            return None
    elif custom_headers is not None:
        _default_header.update(custom_headers)

    if _data is None:
        _req = urllib.request.Request(_url, headers=_default_header)
    else:
        _req = urllib.request.Request(_url, _data.encode(), headers=_default_header)

    if _req is None:
        return None
    else:
        _req.get_method = lambda: _method

        if session is True:
            _cookie = cookie_jar.get_cookie()
            if _cookie is not None:
                _req.add_header('Cookie', _cookie)

        try:
            context = None

            if use_ssl is True:
                context = ssl_lib._create_unverified_context()

            response = urllib.request.urlopen(_req, timeout=_default_timeout, context=context)
            status = response.getcode()

            if status == 200 or status == 201:
                meta = response.info()
                content_type = meta.get('Content-Type')

                if session is True:
                    the_cookie = meta.get("Set-Cookie")
                    if the_cookie:
                        cookie_jar.save_cookie(the_cookie[0])

                if 'application/csv' in content_type:
                    log.warning("The response is a csv file")
                    return None

                elif 'application/json' in content_type:
                    read = response.read()

                    try:
                        resp = json.loads(read)
                        if 'status' in resp:
                            log.info("The response status: {}".format(resp['status']))
                            print("The response status: {}".format(resp['status']))
                        if 'message' in resp:
                            log.info("The response message: {}".format(resp['message']))
                        return resp
                    except ValueError as e:
                        log.warning("The response is not a valid json")
                        log.warning(e)
                        return None

                elif 'application/xml' in content_type or 'text/xml' in content_type:
                    print("The response is a XML")
                    read = response.read()

                    try:
                        xml_root = xmlTree.fromstring(read)
                        return xml_root
                    except ValueError as e:
                        log.warning("The response is not a valid xml")
                        log.warning(e)
                        return read
                    except Exception as e:
                        log.warning("a Exception an ocurred wile read the XML: {0}".format(str(e)))
                        return read

                else:
                    log.warning("content_type" + content_type)
                    log.warning("The response is not a csv file, json or xml response, trying to convert to JSON...")

                    try:
                        resp = response.read()
                        # resp = json.loads(read)
                        return resp
                    except ValueError as e:
                        log.warning("An error occurred while trying to convert the response to JSON")
                        log.warning(e)
                        return None

            else:
                log.warning("The response status Error: {0}".format(str(status)))
                return None

        # except urllib.HTTPError as e:
        except urllib.error.HTTPError as e:
            meta = e.info()
            content_type = meta.get('Content-Type')
            if 'application/json' in content_type:
                read = e.read()
                resp = json.loads(read)
                if 'status' in resp:
                    log.info("The response status: {}".format(resp['status']))
                if 'message' in resp:
                    log.info("The response message: {}".format(resp['message']))
                log.warning("HTTPError: {0} {1}".format(e.code, str(resp)))
                return resp
            #TODO: arreglar la respuesta con status mesage y data
            return e.code
        except Exception as e:
            log.warning("a Exception an ocurred: {0}".format(str(e)))
            return str(e)
        except IOError as e:
            log.warning("can't connect, reason: {0}".format(e.reason))
            return e.reason
