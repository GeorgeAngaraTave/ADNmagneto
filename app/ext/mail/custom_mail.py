# -*- coding: utf-8 -*-

"""Python module for Custom mail."""

from flask_mail import Message
from app import app as app_mail
from app import mail_flask
from app.config.mail import MAIL_ADMIN, DEFAULT_MAIL_MSG, DEFAULT_SUBJECT_MAIL
from app.ext.utils.commons import Commons
import logging as log

from threading import Thread


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


@async
def send_async_email(msg):
    with app_mail.app_context():
        mail_flask.send(msg)


def sendEmail(message, emails_list):
    if message is None:
        log.warning("sendEmail: The message can not be sent blank")
        return None

    if emails_list is None:
        log.warning("sendEmail: The mailing list can not be empty")
        return None

    sender_email = MAIL_ADMIN

    if Commons.validate_email(sender_email):
        subject = DEFAULT_SUBJECT_MAIL

        default_msg = DEFAULT_MAIL_MSG + message

        msg = Message(subject, sender=sender_email, recipients=emails_list)
        msg.body = default_msg
        send_async_email(msg)
    else:
        log.warning('sendEmail: Invalid email')
        return False
