import json
from unittest.mock import Mock, patch
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from atlas.libs.test import RestTestCase


class UploadEmailCSVTest(RestTestCase):

    def setUp(self):
        self.user = RestTestCase.create_admin()
        self.upload_csv_url = reverse('upload_csv')

    def test_upload_email_csv_unauthorized(self):
        data = {
        }
        response = self.client.post(self.upload_csv_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('atlas.api.v3.views.recipients.CSVFilesSerializer')
    @patch('atlas.api.v3.views.recipients.CSVEmailParser')
    def test_upload_email_csv(self, mock_csv_parser, mock_csv_serializer):
        self.authenticate(self.user)
        mock_serializer_instance = mock_csv_serializer.return_value
        mock_parser_instance = mock_csv_parser.return_value

        valid_emails = ['example1@example.com', 'example2@example.com']
        invalid_emails = ['invalidemail']
        csv_file = 'a.csv'
        data = {
            'csv_files': [csv_file],
        }

        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.validated_data = data
        mock_parser_instance.parse_csvs.return_value = valid_emails, invalid_emails

        response = self.client.post(
            self.upload_csv_url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['valid_emails'], valid_emails)
        self.assertEqual(response.data['invalid_emails'], invalid_emails)
        mock_csv_serializer.assert_called_once_with(data=data)
        mock_serializer_instance.is_valid.assert_called_once()
        mock_parser_instance.parse_csvs.assert_called_once_with([csv_file])

    @patch('atlas.api.v3.views.recipients.CSVFilesSerializer')
    def test_upload_email_csv_body_not_valid(self, mock_csv_serializer):
        self.authenticate(self.user)
        mock_csv_serializer.return_value.is_valid.return_value = False
        data = {
            'csv_files': ['a.txt'],
        }
        response = self.client.post(
            self.upload_csv_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)