from unittest.mock import MagicMock, Mock, call, patch
from atlas.apps.email_blaster.models import EmailTemplate
from atlas.apps.email_blaster.serializers import CSVFilesSerializer, EmailSendRequestSerializer, EmailTemplateSerializer, EmailRecipientSerializer
from rest_framework.test import APITestCase
from rest_framework import serializers
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from atlas.apps.survei.models import Survei
from atlas.apps.email_blaster.models import EmailRecipient
from atlas.apps.email_blaster.services import EmailRecipientService
from atlas.libs.test import RestTestCase


class EmailTemplateSerializerTestCase(APITestCase):
    def setUp(self):
        self.email_template = EmailTemplate.objects.create(
            title="Test Template",
            email_subject="Test Subject",
            email_body="Test Body"
        )
        self.serializer = EmailTemplateSerializer(instance=self.email_template)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(
            ['id', 'title', 'email_subject', 'email_body']))

    def test_title_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['title'], self.email_template.title)

    def test_email_subject_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['email_subject'],
                         self.email_template.email_subject)

    def test_email_body_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['email_body'], self.email_template.email_body)


class EmailSendRequestSerializerTestCase(APITestCase):
    def setUp(self):
        self.email_template = EmailTemplate.objects.create(
            title="Test Template",
            email_subject="Test Subject",
            email_body="Test Body"
        )
        self.data = {'email_template_id': 1, 'survei_id': 1, 'recipients': [
            'test1@example.com'], 'wait_delay': 10, 'batch_size': 30}
        self.serializer = EmailTemplateSerializer(instance=self.email_template)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(
            ['id', 'title', 'email_subject', 'email_body']))

    def test_title_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['title'], self.email_template.title)

    def test_email_subject_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['email_subject'],
                         self.email_template.email_subject)

    def test_email_body_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['email_body'], self.email_template.email_body)

    @patch('atlas.apps.email_blaster.serializers.EmailTemplateService')
    def test_email_template_id_validation_success(self, service):
        service.return_value.get_email_template.return_value = {
            'id': 1, 'email_body': 'Test email body', 'email_subject': 'Test email subject'}

        serializer = EmailSendRequestSerializer(data=self.data)
        validated_email_template_id = serializer.validate_email_template_id(
            self.data['email_template_id'])

        self.assertEqual(validated_email_template_id,
                         self.data['email_template_id'])

    @patch('atlas.apps.email_blaster.serializers.EmailTemplateService')
    def test_email_template_id_validation_error(self, service):
        service.return_value.get_email_template.return_value = None

        serializer = EmailSendRequestSerializer(data=self.data)
        with self.assertRaisesMessage(
            serializers.ValidationError,
            "Email template with id {} does not exist".format(
                self.data['email_template_id'])
        ):
            serializer.validate_email_template_id(
                self.data['email_template_id'])

    @patch('atlas.apps.email_blaster.serializers.SurveiService')
    def test_survei_id_validation_success(self, service):
        service.return_value.get_survei.return_value = True

        serializer = EmailSendRequestSerializer(data=self.data)
        validated_survei_id = serializer.validate_survei_id(
            self.data['survei_id'])

        self.assertEqual(validated_survei_id, self.data['survei_id'])

    @patch('atlas.apps.email_blaster.serializers.SurveiService')
    def test_survei_id_validation_error(self, service):
        service.return_value.get_survei.return_value = None

        serializer = EmailSendRequestSerializer(data=self.data)
        with self.assertRaisesMessage(
            serializers.ValidationError,
            "Survei with id {} does not exist".format(
                self.data['survei_id'])
        ):
            serializer.validate_survei_id(self.data['survei_id'])


class CSVFilesSerializerTestCase(APITestCase):
    def setUp(self):
        self.serializer = CSVFilesSerializer()

    def test_validate_csv_files_no_files(self):
        data = {'csv_files': []}
        with self.assertRaises(serializers.ValidationError) as cm:
            self.serializer.validate_csv_files(data['csv_files'])
        self.assertIn("At least one CSV file is required.", str(cm.exception))

    def test_validate_csv_files_valid(self):
        valid_file = SimpleUploadedFile(
            'valid.csv', b'csv content', content_type='text/csv')
        data = {'csv_files': [valid_file]}
        validated_files = self.serializer.validate_csv_files(data['csv_files'])
        self.assertEqual(validated_files, data['csv_files'])

    def test_validate_csv_files_invalid_file(self):
        non_csv_file = SimpleUploadedFile(
            'non_csv.txt', b'text content', content_type='text/plain')
        data = {'csv_files': [non_csv_file]}
        with self.assertRaises(serializers.ValidationError) as cm:
            self.serializer.validate_csv_files(data['csv_files'])
        self.assertIn("File 'non_csv.txt' is not a CSV file.",
                      str(cm.exception))


class TestEmailRecipientSerializer(TestCase):

    def setUp(self):
        self.serializer_data = {
            'id': 1,
            'survei_id': 2,
            'group_recipients_years' : [2021, 2022],
            'group_recipients_terms' : [2, 1],
            'individual_recipients_emails' : ["dimas@gmail.com", "dimas@yahoo.com"],
            'csv_emails' : ["csv@gmail.com", "csv@yahoo.com"]
        }
        self.serializer = EmailRecipientSerializer(data=self.serializer_data)

        self.user = RestTestCase.create_admin()
        self.survei = Survei.objects.create(
            id=self.serializer_data.get("survei_id"),
            nama='Survei Test',
            deskripsi='Deskripsi Survei Test',
            creator=self.user
        )

    def test_request_contains_expected_fields(self):
        fields = self.serializer.get_fields()
        self.assertEqual(set(fields), set(
            ['id', 'survei_id', 'group_recipients_years', 'group_recipients_terms', 'individual_recipients_emails', 'csv_emails']))

    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_initial_request_is_valid(self, get_survei_mock):
        self.assertTrue(self.serializer.is_valid())

    def test_survei_id_is_required(self):
        self.serializer_data.pop('survei_id')
        serializer = EmailRecipientSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    def test_data_is_not_empty(self):
        self.serializer_data = []
        serializer = EmailRecipientSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_validate_called_get_survei_once(self, get_survei_mock):
        self.serializer.is_valid()
        get_survei_mock.assert_called_once()

    @patch('atlas.apps.survei.services.SurveiService.get_survei', Mock(return_value=True))
    def test_validate_should_succeed_if_get_survei_return_value(self):
        self.assertTrue(self.serializer.is_valid())

    @patch('atlas.apps.survei.services.SurveiService.get_survei', Mock(return_value=None))
    def test_validate_should_fail_if_get_survei_return_none(self):
        self.assertFalse(self.serializer.is_valid())

    @patch('atlas.apps.survei.services.SurveiService.get_survei', Mock(return_value=None))
    def test_validate_should_raise_error_if_get_survei_return_none(self):
        self.serializer.is_valid()
        self.assertRaises(serializers.ValidationError)

    @patch('atlas.apps.survei.services.SurveiService.get_survei', Mock(return_value=None))
    def test_validate_survey_id_should_raise_with_correct_message(self):
        with self.assertRaises(serializers.ValidationError) as exc:
            self.serializer.validate_survei_id(2)
        self.assertEqual(
            str(exc.exception.detail[0]), "Survei dengan id 2 tidak ditemukan")

    @patch('atlas.apps.email_blaster.services.EmailRecipientService.create_email_recipient_data')
    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_create_should_call_get_survei_once_with_param(self, get_survei_mock, create_data_mock):
        self.serializer.create(self.serializer_data)
        get_survei_mock.assert_called_once_with(
            self.serializer_data['survei_id'])
        
    @patch('atlas.apps.email_blaster.services.EmailRecipientService.create_email_recipient_data')
    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_create_should_create_email_recipient_data_once(self, get_survei_mock, create_data_mock):
        survei_mock = MagicMock(spec=Survei)
        get_survei_mock.configure_mock(return_value=survei_mock)
        self.serializer.create(self.serializer_data)
        create_data_mock.assert_called_once_with(
            survei=survei_mock,
            group_recipients_years=self.serializer_data.get("group_recipients_years"),
            group_recipients_terms=self.serializer_data.get("group_recipients_terms"),
            individual_recipients_emails=self.serializer_data.get("individual_recipients_emails"),
            csv_emails=self.serializer_data.get("csv_emails"))
        
    @patch('atlas.apps.email_blaster.services.EmailRecipientService.exclude_alumni_that_has_responded')
    @patch('atlas.apps.email_blaster.services.EmailRecipientService.get_email_recipients')
    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    @patch('atlas.apps.email_blaster.services.EmailRecipientService.create_email_recipient_data')
    def test_create_should_return_as_expected(self, create_data_mock, get_survei_mock, get_email_recipients_mock, exclude_alumni_mock):
        
        expected_emails = []
        expected_emails.extend(self.serializer_data["individual_recipients_emails"])
        expected_emails.extend(self.serializer_data["csv_emails"])

        survei_mock = MagicMock(spec=Survei)
        survei_mock.id = 1
        get_survei_mock.return_value = survei_mock

        email_recipient_data_mock = MagicMock()
        email_recipient_data_mock.group_recipients_years = [2020, 2021]
        email_recipient_data_mock.group_recipients_terms = [1, 2]
        email_recipient_data_mock.individual_recipients_emails = self.serializer_data["individual_recipients_emails"]
        email_recipient_data_mock.csv_emails = self.serializer_data["csv_emails"]
        create_data_mock.return_value = email_recipient_data_mock

        get_email_recipients_mock.return_value = expected_emails
        exclude_alumni_mock.return_value = expected_emails
        email_fetched = self.serializer.create(self.serializer_data)

        self.assertEqual(email_fetched.get("emails"), expected_emails)