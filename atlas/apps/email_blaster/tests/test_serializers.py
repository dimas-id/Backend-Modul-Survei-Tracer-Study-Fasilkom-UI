from unittest.mock import patch
from atlas.apps.email_blaster.models import EmailTemplate
from atlas.apps.email_blaster.serializers import EmailSendRequestSerializer, EmailTemplateSerializer
from rest_framework.test import APITestCase
from rest_framework import serializers


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
