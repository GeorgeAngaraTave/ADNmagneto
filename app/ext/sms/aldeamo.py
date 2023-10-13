# -*- coding: utf-8 -*-

"""Python module for Aldeamo SMS Api."""

import xml.etree.ElementTree as xmlTree
from app.config.sms import ALDEAMO_SMS_URL_API, ALDEAMO_USERNAME_API, ALDEAMO_PASSWORD_API
from app.ext.rest import consumer
from app.ext.utils import Commons
import logging as log

sms_key_list = ('country', 'mobile', 'message')

headers = {
    'Content-Type': 'application/xml',
    'Accept': '*/*'
}


class AldeamoSMS:

    @staticmethod
    def single_sms(message_data=None):

        if message_data is None:
            log.warning("AldeamoSMS: missing fields 'message_data'")
            return None

        if type(message_data) is not dict:
            log.warning("AldeamoSMS: fields 'message_data' is not a dict")
            return None

        if all(param in message_data for param in sms_key_list):

            default_message = """
                <sending>
                    <authentication>
                        <username>{0}</username>
                        <password>{1}</password>
                    </authentication>
                    <country>{2}</country>
                    <recipients>
                        <sms>
                            <mobile>{3}</mobile>
                            <message>{4}</message>
                        </sms>
                    </recipients>
                </sending>
            """.format(ALDEAMO_USERNAME_API, ALDEAMO_PASSWORD_API, message_data['country'], message_data['mobile'], message_data['message'])

            xml_root = xmlTree.fromstring(default_message)

            if 'operator' in message_data:
                recipients = xml_root.find('recipients')
                sms = recipients.find('sms')
                operator = xmlTree.SubElement(sms, 'operator')
                operator.text = message_data['operator']

            str_xml = xmlTree.tostring(xml_root, encoding='ISO-8859-1', method='xml')

            resp = consumer(ALDEAMO_SMS_URL_API, 'POST', str_xml, headers, use_ssl=True, options='xml')

            return resp

        else:
            log.warning("AldeamoSMS: missing fields in 'message_data': %s", str(sms_key_list))
            return None

    @staticmethod
    def masive_sms(message_list=200):

        if message_list is None:
            log.warning("AldeamoSMS: missing fields 'message_list'")
            return None

        if type(message_list) is not dict:
            log.warning("AldeamoSMS: fields 'message_list' is not a dict")
            return None

        if all(param in message_list for param in sms_key_list):
            mobile_list = message_list['mobile']

            if Commons.is_iterable(mobile_list):
                if len(mobile_list) > 0:
                    default_message = """
                        <sending>
                            <authentication>
                                <username>{0}</username>
                                <password>{1}</password>
                            </authentication>
                            <country>{2}</country>
                        </sending>
                    """.format(ALDEAMO_USERNAME_API, ALDEAMO_PASSWORD_API, message_list['country'])

                    try:
                        xml_root = xmlTree.fromstring(default_message)
                        recipients = xmlTree.SubElement(xml_root, 'recipients')

                        for phone in mobile_list:
                            sms = xmlTree.SubElement(recipients, 'sms')

                            mobile = xmlTree.SubElement(sms, 'mobile')
                            mobile.text = phone

                            message = xmlTree.SubElement(sms, 'message')
                            message.text = message_list['message']

                        str_xml = xmlTree.tostring(xml_root, encoding='ISO-8859-1', method='xml')

                        resp = consumer(ALDEAMO_SMS_URL_API, 'POST', str_xml, headers, use_ssl=True, options='xml')

                        return resp

                    except Exception as e:
                        log.warning("AldeamoSMS Exception: %s", str(e))
                        return str(e)
                else:
                    log.warning("AldeamoSMS: fields 'mobile_list' is empty")
                    return None
            else:
                log.warning("AldeamoSMS: 'mobile_list' is not iterable")
                return None
        else:
            log.warning("AldeamoSMS: missing fields in 'message_list': %s", str(sms_key_list))
            return None
