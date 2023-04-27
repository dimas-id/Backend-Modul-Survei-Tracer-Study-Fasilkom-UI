from smtplib import SMTPException

from atlas.apps.email_blaster.models import EmailTemplate
from .celery import app
from django.core.mail import EmailMessage
from django.db import (transaction)


@app.task(autoretry_for=(SMTPException,), retry_backoff=5, max_retries=5)
def send_email_task(subject, body, recipients):
    message = EmailMessage(subject, body, bcc=recipients)
    return message.send(fail_silently=False)


class EmailSendService:
    def __init__(self, email_body_with_placeholder, survei_url, email_subject, recipients):
        self.email_body = self._replace_url_email_body(
            email_body_with_placeholder, survei_url)
        self.email_subject = email_subject
        self.recipients = recipients

    def _replace_url_email_body(self, email_body, survei_url):
        return email_body.replace("{{URL_SURVEI}}", survei_url)

    def send_email_batch(self, wait_delay=10, batch_size=30):
        for i in range(0, len(self.recipients), batch_size):
            send_email_task.apply_async(
                args=(self.email_subject, self.email_body,
                      self.recipients[i:i + batch_size]),
                countdown=wait_delay*i)


class EmailTemplateService:
    @transaction.atomic
    def get_email_template(self, email_template_id):
        try:
            email_template = EmailTemplate.objects.get(id=email_template_id)
            return email_template
        except EmailTemplate.DoesNotExist:
            return None
