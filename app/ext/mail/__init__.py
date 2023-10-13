try:
    from .sendgrid_mail import SendGridMail
except ImportError:
    import logging as log
    log.warning('Warning: Loading custom_mail')
    from .custom_mail import sendEmail
