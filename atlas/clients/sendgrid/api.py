import logging

from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *

from atlas.libs.client import AbstractClientManager


def client_factory():
    return SendGridAPIClient(settings.SENDGRID_API_KEY)


def mail_factory(**extra):
    extra.setdefault('from_email', 'iluni12@cs.ui.ac.id')
    return Mail(**extra)


class MailManager(AbstractClientManager):
    client = client_factory()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls_name = self.__class__.__name__
        self.logger = logging.getLogger(cls_name)

    def send_email(self, subject, html_content, to_emails, fail_silently=False, from_email=None):

        if not settings.PRODUCTION:
            # just dont send email
            return

        extra = {}
        if from_email is not None:
            extra['from_email'] = from_email
        mail = mail_factory(
                subject=subject, html_content=html_content, to_emails=to_emails, **extra)

        try:
            return self.get_client().send(mail)
        except Exception as e:
            self.logger.error(e.message)
            if not fail_silently:
                raise e
