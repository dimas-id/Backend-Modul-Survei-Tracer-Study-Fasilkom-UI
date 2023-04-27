import json
from unittest.mock import Mock, patch
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from atlas.libs.test import RestTestCase


class SendEmailTest(RestTestCase):

    def setUp(self):
        self.user = RestTestCase.create_admin()
        self.send_email_url = reverse('send_email')
        self.preview_email_url = reverse('preview_email')

    def test_send_email_unauthorized(self):
        data = {
        }
        response = self.client.post(self.send_email_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('atlas.api.v3.views.email_blaster.EmailSendService')
    @patch('atlas.api.v3.views.email_blaster.EmailTemplateService')
    @patch('atlas.api.v3.views.email_blaster.EmailSendRequestSerializer')
    def test_send_email_success(self, mock_serializer, email_template_service_mock, email_send_service_mock):
        self.authenticate(self.user)
        mock_serializer.return_value.is_valid.return_value = True

        data = {
            "email_template_id": 1,
            "survei_id": 1,
            "recipients": ["test1@example.com", "test2@example.com"],
            "wait_delay": 0,
            "batch_size": 1
        }

        response = self.client.post(self.send_email_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_send_email_missing_required_fields(self):

        self.authenticate(self.user)
        data = {
            "survei_id": 1,
            "recipients": ["test1@example.com", "test3@example.com"],
            "wait_delay": 0,
            "batch_size": 1
        }
        response = self.client.post(self.send_email_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('emailTemplateId', json.loads(
            response.content)['messages'])

    def test_send_email_invalid_email_template_id(self):
        self.authenticate(self.user)
        data = {
            "email_template_id": 999,
            "survei_id": 1,
            "recipients": ["test11@example.com", "tes@example.com"],
            "wait_delay": 0,
            "batch_size": 1
        }
        response = self.client.post(self.send_email_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('emailTemplateId', json.loads(
            response.content)['messages'])

    def test_send_email_invalid_survei_id(self):
        self.authenticate(self.user)
        data = {
            "email_template_id": 1,
            "survei_id": -1,
            "recipients": ["test11@example.com", "tes@example.com"],
            "wait_delay": 0,
            "batch_size": 1
        }
        response = self.client.post(self.send_email_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('surveiId', json.loads(
            response.content)['messages'])

    def test_send_email_invalid_recipients(self):
        self.authenticate(self.user)
        data = {
            "email_template_id": 1,
            "survei_id": 1,
            "recipients": "invalid_recipients",
            "wait_delay": 0,
            "batch_size": 1
        }
        response = self.client.post(self.send_email_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('recipients', json.loads(response.content)['messages'])

    def test_preview_email_unauthorized(self):
        data = {
        }
        response = self.client.post(
            self.preview_email_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('atlas.api.v3.views.email_blaster.EmailSendService')
    @patch('atlas.api.v3.views.email_blaster.EmailTemplateService')
    @patch('atlas.api.v3.views.email_blaster.EmailSendRequestSerializer')
    def test_preview_email_success(self, mock_serializer, email_template_service_mock, email_send_service_mock):
        self.authenticate(self.user)
        mock_serializer.return_value.is_valid.return_value = True

        data = {
            "email_template_id": 1,
            "survei_id": 1,
            "recipients": ["test1@example.com", "test2@example.com"],
            "wait_delay": 0,
            "batch_size": 1
        }

        response = self.client.post(
            self.preview_email_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_preview_email_missing_required_fields(self):

        self.authenticate(self.user)
        data = {
            "survei_id": 1,
            "recipients": ["test1@example.com", "test3@example.com"],
            "wait_delay": 0,
            "batch_size": 1
        }
        response = self.client.post(
            self.preview_email_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('emailTemplateId', json.loads(
            response.content)['messages'])

    def test_preview_email_invalid_email_template_id(self):
        self.authenticate(self.user)
        data = {
            "email_template_id": 999,
            "survei_id": 1,
            "recipients": ["test11@example.com", "tes@example.com"],
            "wait_delay": 0,
            "batch_size": 1
        }
        response = self.client.post(
            self.preview_email_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('emailTemplateId', json.loads(
            response.content)['messages'])

    def test_preview_email_invalid_survei_id(self):
        self.authenticate(self.user)
        data = {
            "email_template_id": 1,
            "survei_id": -1,
            "recipients": ["test11@example.com", "tes@example.com"],
            "wait_delay": 0,
            "batch_size": 1
        }
        response = self.client.post(
            self.preview_email_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('surveiId', json.loads(
            response.content)['messages'])

    def test_preview_email_invalid_recipients(self):
        self.authenticate(self.user)
        data = {
            "email_template_id": 1,
            "survei_id": 1,
            "recipients": "invalid_recipients",
            "wait_delay": 0,
            "batch_size": 1
        }
        response = self.client.post(
            self.preview_email_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('recipients', json.loads(response.content)['messages'])
