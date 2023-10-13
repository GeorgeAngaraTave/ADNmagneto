# -*- coding: utf-8 -*-

"""Python module for Firebase Realtime Database."""

from app.ext.rest import consumer
from app.config.google.firebase import REALTIME_URI, FIREBASE_API_KEY
import logging as log

headers = {
    'access_token': FIREBASE_API_KEY
}


def realtime_api(notification_name=None, data=None):
    if notification_name is None:
        return None

    if data is None:
        return None

    try:
        URI = "{0}/{1}/{2}.json".format(REALTIME_URI, 'messages', str(notification_name))

        resp = consumer(URI, 'POST', data, headers, use_ssl=True)

        if resp is None:
            print(resp)
            log.info("Firebase realtime result none")
            return None
        else:
            print('realtime_api response:', resp)
            return resp
    except Exception as e:
        print("realtime_api Exception:", e)
        return None
