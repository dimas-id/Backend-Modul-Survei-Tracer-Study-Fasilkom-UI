import csv
from email_validator import validate_email, EmailNotValidError
from smtplib import SMTPException
from django.core.validators import EmailValidator
from atlas.apps.email_blaster.models import EmailTemplate, EmailRecipient
from .celery import app
from django.core.mail import EmailMessage
from django.db import transaction
from atlas.apps.account.models import User
from atlas.apps.experience.models import Education
from atlas.apps.response.models import Response
from atlas.apps.survei.models import Survei


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

    
class EmailRecipientService:

    @transaction.atomic
    def create_email_recipient_data(self, survei, group_recipients_years, group_recipients_terms, individual_recipients_emails, csv_emails):

        """Create the EmailRecipient object to save the data"""

        return EmailRecipient.objects.create(
            survei=survei, 
            group_recipients_years=group_recipients_years, 
            group_recipients_terms=group_recipients_terms, 
            individual_recipients_emails=individual_recipients_emails,
            csv_emails=csv_emails)

    @transaction.atomic
    def get_email_recipients(self, group_years, group_terms, individuals, csv_emails):
        
        """Fetch all of the emails"""
        
        email_recipients = []
        
        alumni_emails = self.get_group_of_alumni_by_graduation_year_and_term(group_years, group_terms)
        emails_per_group = alumni_emails.values()

        for email_group in emails_per_group:
            email_recipients.extend(email_group)

        email_recipients.extend(individuals)
        email_recipients.extend(csv_emails)
        
        return list(set(email_recipients))

    @transaction.atomic
    def get_all_student_by_graduation_year_and_term(self, tahun, term):

        """Get group of students by specific graduation year and term, 
        e.g. graduate students batch of 2021 term 2"""

        alumni_user = Education.objects.filter(
            csui_graduation_year=tahun,
            csui_graduation_term=term)
        
        alumni_emails = []

        for user in alumni_user:
            alumni_emails.append(self.get_user_email_by_id(user.user_id))   

        return alumni_emails
    
    @transaction.atomic
    def get_group_of_alumni_by_graduation_year_and_term(self, tahun_list, term_list):

        """Get group of students by the desired numbers of group of graduation years and terms, 
        by a note that in every index of the tahun_list and term_list will connected to each other
        (e.g. tahun list = [2021, 2022], term list = [1, 2] then we will get the students from the 2021 term 1, and 2022 term 2)"""
        
        alumni_group_by_year = {}

        total_request = len(tahun_list)
        for request_number in range(total_request):
            tahun = tahun_list[request_number]
            term = term_list[request_number]

            group = "{} term {}".format(str(tahun), str(term))
            alumni_group_by_year[group] = self.get_all_student_by_graduation_year_and_term(tahun, term)

            if len(alumni_group_by_year[group]) == 0 :
                alumni_group_by_year.pop(group)

        return alumni_group_by_year
    
    @transaction.atomic
    def get_user_email_by_id(self, user):

        """Checked if email exist by the user_id, then get the user email."""

        try:
            user_email = User.objects.get(id=user)
            return user_email.email

        except:
            return None
        
    @transaction.atomic
    def response_checker(self, emails, survei_id):

        """Checking the response of the survey, returns all of the emails that has responded to the survey"""

        survei = Survei.objects.get(id=survei_id)
        responses = Response.objects.filter(survei=survei)

        emails_responded = []

        for response in responses:
            if response.user.email in emails:
                emails_responded.append(response.user.email)

        return emails_responded

    @transaction.atomic
    def get_total_alumni_of_a_group_that_havent_filled_survey(self, alumni, survei_id):
        
        """Checking the total number of alumni from a group of graduation year-term that haven't filled the survey yet"""

        alumni_responded = self.response_checker(alumni.copy(), survei_id)
        return len(list(set(alumni.copy()) - set(alumni_responded)))
    
    @transaction.atomic
    def exclude_alumni_that_has_responded(self, alumni, survei_id):
        
        """Make sure that all of the alumni who has responded is not included as the email recipients"""

        alumni_responded = self.response_checker(alumni.copy(), survei_id)
        return list(set(alumni.copy()) - set(alumni_responded))