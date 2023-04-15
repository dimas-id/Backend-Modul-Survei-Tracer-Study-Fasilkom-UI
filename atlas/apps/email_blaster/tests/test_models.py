from django.test import TestCase
from atlas.apps.email_blaster.models import EmailTemplate


class EmailTemplateModelTestCase(TestCase):
    def setUp(self):
        self.email_template = EmailTemplate.objects.create(
            title="Test Template",
            email_subject="Test Subject",
            email_body="Test Body"
        )

    def test_title_field(self):
        field_label = self.email_template._meta.get_field('title').verbose_name
        max_length = self.email_template._meta.get_field('title').max_length
        self.assertEqual(field_label, 'title')
        self.assertEqual(max_length, 150)

    def test_email_subject_field(self):
        field_label = self.email_template._meta.get_field(
            'email_subject').verbose_name
        max_length = self.email_template._meta.get_field(
            'email_subject').max_length
        self.assertEqual(field_label, 'email subject')
        self.assertEqual(max_length, 150)

    def test_email_body_field(self):
        field_label = self.email_template._meta.get_field(
            'email_body').verbose_name
        self.assertEqual(field_label, 'email body')
        self.assertTrue(self.email_template.email_body)

    def test_object_name(self):
        expected_object_name = f"{self.email_template.title} - {self.email_template.email_subject}"
        self.assertEqual(str(self.email_template), expected_object_name)
