# -*- coding: utf-8 -*-

"""Python module for Firebase Cloud Messaging."""

from app.config.google.firebase import MESSAGE_URI, SUBSCRIBE_URI
from app.config.google.firebase import DEFAULT_TOPICS_NAME, TOKEN_SERVER
from app.ext.rest import consumer
import logging as log

default_message = {
    "notification": {
        "title": "message from BackEndBase",
        "body": None,
        "click_action": "http://localhost:9876/"
    },
    "to": "/topics/"
}

headers = {
    'Authorization': 'key=' + TOKEN_SERVER
}


def send_to_topic(message=None, topic_name=None):
    if message is None:
        return None

    if topic_name is None:
        return None

    if type(message) is not dict:
        return None

    if len(message) <= 0:
        return None

    default_message['notification']['body'] = message
    default_message['to'] = "/topics/{0}".format(topic_name)

    resp = consumer(MESSAGE_URI, 'POST', default_message, headers, use_ssl=True)

    if resp is None:
        return None

    if 'message_id' in resp:
        log.info("The response message id: {0}".format(resp['message_id']))
        response = {
            "message_id": resp['message_id']
        }
    else:
        response = {
            "error": resp
        }

    return response


def subscribe_to_topic(client_token=None):
    if client_token is None:
        return None

    for topic in DEFAULT_TOPICS_NAME:
        uri = SUBSCRIBE_URI.format(client_token, topic)

        resp = consumer(uri, 'POST', custom_headers=headers, use_ssl=True)

        log.info("The response subscribe: {0}".format(resp))

    return True


def send_to_receiver(message=None, registration_id=None):
    if message is None:
        return None

    if registration_id is None:
        return None

    if type(message) is not dict:
        return None

    if len(message) <= 0:
        return None

    default_message['notification']['body'] = message
    default_message['to'] = "{0}".format(registration_id)

    resp = consumer(MESSAGE_URI, 'POST', default_message, headers, use_ssl=True)

    if resp is None:
        return None
    else:
        if 'success' in resp:
            log.info("The response multicast_id: {0}".format(resp['multicast_id']))
            return resp['multicast_id']
        else:
            return resp
