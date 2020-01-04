import json
import random
from unittest.mock import patch

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from atlas.libs.test import RestTestCase
from atlas.libs.test import UserFactory
from atlas.apps.account.models import User


class TestUserCreateView(RestTestCase):

    def setUp(self) -> None:
        super().setUp()
        # turn off throttle scope so we dont get code 429 after certain tests
        from atlas.api.v1.views.account import UserCreateView
        UserCreateView.throttle_scope = None

    @patch('atlas.apps.account.signals.redis.enqueue')
    def test_register_user_success(self, mock_enqueue):
        data = {
            'email': 'wisnu1c@csui.com',
            'password': 'adwawdbbb23123131',
            'firstName': 'wisnu',
            'lastName': 'pramadhitya',
            'birthdate': '1998-01-14',
            'linkedinUrl': 'https://linkedin.com/in/wisnuprama'
        }

        uri = reverse('account_register_v2')
        response = self.client.post(path=uri, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('atlas.apps.account.signals.redis.enqueue')
    def test_register_user_success_with_linkedin_url(self, mock_enqueue):
        data = {
            'email': 'wisnu1c@csui.com',
            'password': 'adwawdbbb23123131',
            'firstName': 'wisnu',
            'lastName': 'pramadhitya',
            'birthdate': '1998-01-14',
            'linkedinUrl': 'https://linkedin.com/in/wisnuprama'
        }

        uri = reverse('account_register_v2')
        response = self.client.post(path=uri, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        users = User.objects.filter(email='wisnu1c@csui.com')
        self.assertEqual(users.count(), 1)

        user = users.first()
        self.assertEqual(user.profile.linkedin_url,
                         'https://linkedin.com/in/wisnuprama')

    @patch('atlas.apps.account.signals.redis.enqueue')
    def test_register_user_low_quality_password(self, mock_enqueue):
        data = {
            'email': 'wisnu1c@csui.com',
            'password': 'abcde123',
            'firstName': 'wisnu',
            'lastName': 'pramadhitya',
            'birthdate': '1998-01-14',
        }

        uri = reverse('account_register_v2')
        response = self.client.post(path=uri, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue('password' in json.loads(response.content))

    @patch('atlas.apps.account.signals.redis.enqueue')
    def test_register_user_email_is_unique(self, mock_enqueue):
        TestUserCreateView.create_user(email='wisnu1c@csui.com')
        data = {
            'email': 'wisnu1c@csui.com',
            'password': 'adwawdbbb23123131',
            'firstName': 'wisnu',
            'lastName': 'pramadhitya',
            'birthdate': '1998-01-14',
        }

        uri = reverse('account_register_v2')
        response = self.client.post(path=uri, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('email' in json.loads(response.content))

    @patch('atlas.apps.account.signals.redis.enqueue')
    def test_register_user_linkedin_url(self, mock_enqueue):
        data = {
            'email': 'wisnu1c@csui.com',
            'password': 'adwawdbbb23123131',
            'firstName': 'wisnu',
            'lastName': 'pramadhitya',
            'birthdate': '1998-01-14',
            'linkedinUrl': 'https://linkedin.com/'
        }

        uri = reverse('account_register_v2')
        response = self.client.post(path=uri, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('linkedinUrl' in json.loads(response.content))
