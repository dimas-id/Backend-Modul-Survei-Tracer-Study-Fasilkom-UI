from django.test import TestCase
from atlas.apps.email_blaster.models import EmailTemplate, EmailRecipient
from atlas.apps.account.models import User
from atlas.apps.survei.models import Survei


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


class TestEmailRecipientModels(TestCase):

    def setUp(self):
        

        user_data = {
            'first_name': "dimas",
            'last_name': 'ilham',
            'email': 'dimas@gmail.com'
        }

        survei_data = {
            'nama': 'survei 2',
            'deskripsi': 'ini adalah survei',
        }

        email_recipient_data = {
            'tanggal_dikirim' : "2023-03-18 20:48:35",
            'group_recipients_years' : [2021, 2022],
            'group_recipients_terms' : [2, 1],
            'individual_recipients_emails' : ["dimas@gmail.com", "dimas@yahoo.com"]
        }

        user = User.objects.create(**user_data)
        self.survei = Survei.objects.create(
            **survei_data, creator=user)
        self.email_recipient_data = EmailRecipient.objects.create(
            **email_recipient_data, survei = self.survei)

    def test_valid_model_str(self):
        self.assertEqual(
            str(EmailRecipient.objects.get(tanggal_dikirim=self.email_recipient_data.tanggal_dikirim)), 
            "survei 2 - {}".format(self.email_recipient_data.tanggal_dikirim))