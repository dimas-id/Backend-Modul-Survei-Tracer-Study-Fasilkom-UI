from unittest.mock import call, patch, Mock
from django.test import TestCase
from atlas.apps.email_blaster.models import EmailTemplate
from atlas.apps.email_blaster.services import CSVEmailParser, EmailTemplateService, send_email_task, EmailSendService
from django.core.files.uploadedfile import SimpleUploadedFile


class EmailSendTaskTestCase(TestCase):

    @patch('atlas.apps.email_blaster.services.EmailMessage')
    def test_send_email_task(self, mock_email_message):
        subject = 'Test subject'
        body = 'Test body'
        recipients = ['email1@example.com', 'email2@example.com']
        mock_email_message_instance = Mock()
        mock_email_message_instance.send.return_value = 1
        mock_email_message.return_value = mock_email_message_instance
        result = send_email_task(subject, body, recipients)
        self.assertEqual(result, 1)
        mock_email_message.assert_called_once_with(
            subject, body, bcc=recipients)
        mock_email_message_instance.send.assert_called_once_with(
            fail_silently=False)


class EmailSendServiceTestCase(TestCase):

    def setUp(self):
        self.name = 'Test template'
        self.email_subject = 'Test email subject'
        self.email_body = 'Test email body {{URL_SURVEI}}'
        self.survei_url = 'http://example.com/survei/123'
        self.recipients = ['email1@example.com', 'email2@example.com']
        self.correct_body = 'Test email body http://example.com/survei/123'

    def test_email_send_service(self):

        email_send_service = EmailSendService(
            email_body_with_placeholder=self.email_body,
            survei_url=self.survei_url,
            email_subject=self.email_subject,
            recipients=self.recipients
        )
        with patch('atlas.apps.email_blaster.services.send_email_task.apply_async') as mock_send_email_task:
            email_send_service.send_email_batch(wait_delay=10, batch_size=2)
            mock_send_email_task.assert_called_once_with(
                args=(self.email_subject,
                      self.correct_body, self.recipients),
                countdown=0
            )
            mock_send_email_task.reset_mock()
            email_send_service.send_email_batch(wait_delay=10, batch_size=1)
            mock_send_email_task.assert_has_calls([
                call(args=(self.email_subject, self.correct_body, [self.recipients[0]]),
                     countdown=0),
                call(args=(self.email_subject, self.correct_body, [self.recipients[1]]),
                     countdown=10)
            ])


class EmailTemplateServiceTestCase(TestCase):

    def setUp(self):
        self.service = EmailTemplateService()

    def test_get_email_template_returns_template(self):
        template = EmailTemplate.objects.create(
            title="Test Template",
            email_subject="Test Subject",
            email_body="Test Body"
        )

        with patch.object(EmailTemplate.objects, 'get', return_value=template):
            result = self.service.get_email_template(1)

        self.assertEqual(result, template)

    def test_get_email_template_returns_none(self):
        with patch.object(EmailTemplate.objects, 'get', side_effect=EmailTemplate.DoesNotExist):
            result = self.service.get_email_template(100)

        self.assertIsNone(result)


class CSVEmailParserTest(TestCase):

    def setUp(self):
        self.CSV_CONTENT = 'text/csv'
        self.valid_email = ['email1@example.com', 'email2@example.com']
        self.invalid_email = ['invalid_email1', 'invalid_email2']

        self.parser = CSVEmailParser()

        self.mixed_csv_file = SimpleUploadedFile(
            'mixed.csv',
            f"{','.join(self.invalid_email)},{','.join(self.valid_email)}".encode(
                'utf-8'),
            content_type=self.CSV_CONTENT)

        self.invalid_csv_file = SimpleUploadedFile(
            'invalid.csv',
            f"{','.join(self.invalid_email)}".encode('utf-8'),
            content_type=self.CSV_CONTENT)

        self.valid_csv_file = SimpleUploadedFile(
            'valid.csv', f"{','.join(self.valid_email)}".encode('utf-8'),
            content_type=self.CSV_CONTENT
        )

    def test_parse_csv_mixed(self):
        valid_emails, invalid_emails = self.parser.parse_csv(
            self.mixed_csv_file)
        self.assertEqual(
            valid_emails, self.valid_email)
        self.assertEqual(invalid_emails, self.invalid_email)

    def test_parse_csv_valid_email(self):
        valid_emails, invalid_emails = self.parser.parse_csv(
            self.valid_csv_file)
        self.assertEqual(valid_emails, self.valid_email)
        self.assertEqual(invalid_emails, [])

    def test_parse_csv_invalid_email(self):
        valid_emails, invalid_emails = self.parser.parse_csv(
            self.invalid_csv_file)
        self.assertEqual(valid_emails, [])
        self.assertEqual(invalid_emails, self.invalid_email)

    def test_parse_csvs_mixed(self):
        files = [self.valid_csv_file, self.invalid_csv_file]
        valid_emails, invalid_emails = self.parser.parse_csvs(files)
        self.assertEqual(
            valid_emails, self.valid_email)
        self.assertEqual(invalid_emails, self.invalid_email)

    def test_is_valid_email_valid(self):
        self.assertTrue(self.parser.is_valid_email('email@example.com'))

    def test_is_valid_email_invalid(self):
        self.assertFalse(self.parser.is_valid_email('invalid_email'))
