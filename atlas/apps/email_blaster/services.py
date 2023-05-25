import csv
from email_validator import validate_email, EmailNotValidError
from smtplib import SMTPException
from django.core.validators import EmailValidator
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


class CSVEmailParser:
    """Service to parse CSV file(s) and return list of valid emails and list of invalid emails
    """

    def parse_csv(self, file):
        """Parse CSV file and return list of valid emails and list of invalid emails

        Args:
            file {string} -- CSV file

        Returns:
            tuple -- (list of valid emails, list of invalid emails)
        """
        valid_emails = []
        invalid_emails = []

        data = file.read().decode('utf-8')
        lines = data.splitlines()
        reader = csv.reader(lines)

        for row in reader:
            for email in row:
                email = email.strip()
                if self.is_valid_email(email):
                    valid_emails.append(email)
                else:
                    invalid_emails.append(email)

        return valid_emails, invalid_emails

    def parse_csvs(self, files):
        """Parse list of CSV files and return list of valid emails and list of invalid emails

        Args:
            files {list} -- list of CSV files

        Returns:
            tuple -- (list of valid emails, list of invalid emails)
        """
        valid_emails = []
        invalid_emails = []

        for file in files:
            valid, invalid = self.parse_csv(file)
            valid_emails.extend(valid)
            invalid_emails.extend(invalid)

        return valid_emails, invalid_emails

    @staticmethod
    def is_valid_email(value):
        """Check if email is valid

        Args:
            value {string} -- email address

        Returns:
            boolean -- True if email is valid, False if not
        """

        try:
            validate_email(value, check_deliverability=False)
            return True
        except EmailNotValidError:
            return False
