# -*- coding: utf-8 -*-

"""Python module for Google mail."""

from google.appengine.api import mail
import logging as log
from app.config.mail import MAIL_ADMIN, DEFAULT_MAIL_MSG, DEFAULT_SUBJECT_MAIL


def sendEmail(message, emails_list):
    if message is None:
        log.warning("sendEmail: The message can not be sent blank")
        return None

    if emails_list is None:
        log.warning("sendEmail: The mailing list can not be empty")
        return None

    sender_email = MAIL_ADMIN

    if mail.is_email_valid(sender_email):
        default_msg = DEFAULT_MAIL_MSG + message
        x = {
            'sender': sender_email,
            'to': emails_list,
            'subject': DEFAULT_SUBJECT_MAIL,
            'body': default_msg
        }
        mail.send_mail(**x)
    else:
        log.warning('sendEmail: Invalid email')
