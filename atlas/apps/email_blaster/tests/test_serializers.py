from atlas.apps.email_blaster.models import EmailTemplate
from atlas.apps.email_blaster.serializers import EmailTemplateSerializer
from rest_framework.test import APITestCase


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
