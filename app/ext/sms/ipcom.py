# -*- coding: utf-8 -*-

"""Python module for IPCOM SMS Api."""

import logging as log
from urllib.parse import quote

from app.config.sms import IPCOM_URL_API, IPCOM_USERNAME_API, IPCOM_PASSWORD_API
from app.ext.rest import consumer

TRANSACTION_TYPE = 400
PRODUCT_ID = 3237

sms_key_list = ('country', 'mobile', 'message')
basel_url = "{0}transaction_type={1}&user_id={2}&user_pw={3}&product_id={4}&number={5}&msg={6}"


class IPCOMSMS:

    @staticmethod
    def single_sms(message_data=None):

        if message_data is None:
            log.warning("IPCOMSMS: missing fields 'message_data'")
            return None

        if type(message_data) is not dict:
            log.warning("IPCOMSMS: fields 'message_data' is not a dict")
            return None

        if all(param in message_data for param in sms_key_list):
            try:
                number = "{0}{1}".format(message_data['country'], message_data['mobile'])

                quote_msg = quote(message_data['message'])

                default_message = basel_url.format(IPCOM_URL_API, TRANSACTION_TYPE, IPCOM_USERNAME_API, IPCOM_PASSWORD_API, PRODUCT_ID, number, quote_msg)

                resp = consumer(default_message, 'GET', use_ssl=True)

                if b'Transaction accepted' in resp:
                    return None
                else:
                    print("IPCOMSMS: An error occurred", resp)
                    return "An error occurred: {0}".format(resp)

            except Exception as e:
                log.warning("IPCOMSMS: single_sms Exception", e)
                return str(e)

        else:
            log.warning("IPCOMSMS: missing fields in 'message_data': %s", str(sms_key_list))
            return None

    @staticmethod
    def masive_sms(message_list=None):
        log.warning("IPCOMSMS: not implemented yet")
        return None
