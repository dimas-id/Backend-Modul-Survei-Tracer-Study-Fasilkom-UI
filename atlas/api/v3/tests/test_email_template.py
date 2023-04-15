from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from atlas.apps.email_blaster.models import EmailTemplate
from atlas.libs.test import RestTestCase


class EmailTemplateViewTestCase(RestTestCase):
    def setUp(self):
        self.user = RestTestCase.create_admin()

        self.template = EmailTemplate.objects.create(
            title='Test Template',
            email_subject='Test Subject',
            email_body='Test Body'
        )
        self.url_list = reverse('email_templates_list')
        self.url_create = reverse('email_templates_create')
        self.url_update = reverse(
            'email_templates_update', args=[self.template.id])
        self.url_delete = reverse(
            'email_templates_delete', args=[self.template.id])

    def test_list_templates_unauthorized(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_template_unauthorized(self):
        data = {
            'title': 'New Test Template2',
            'email_subject': 'New Test Subject2',
            'email_body': 'New Test Body2'
        }
        response = self.client.post(self.url_create, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_template_unauthorized(self):
        data = {
            'title': 'Updated Test Template2',
            'email_subject': 'Updated Test Subject2',
            'email_body': 'Updated Test Body2'
        }
        response = self.client.put(self.url_update, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_template_unauthorized(self):
        response = self.client.delete(self.url_delete)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_templates(self):
        self.authenticate(self.user)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_template(self):
        self.authenticate(self.user)
        data = {
            'title': 'New Test Template',
            'email_subject': 'New Test Subject',
            'email_body': 'New Test Body'
        }
        response = self.client.post(self.url_create, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_template(self):
        self.authenticate(self.user)
        data = {
            'title': 'Updated Test Template',
            'email_subject': 'Updated Test Subject',
            'email_body': 'Updated Test Body'
        }
        response = self.client.put(self.url_update, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_template(self):
        self.authenticate(self.user)
        response = self.client.delete(self.url_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
