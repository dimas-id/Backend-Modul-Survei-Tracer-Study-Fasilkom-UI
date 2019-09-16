import json
import random
from unittest.mock import patch

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from atlas.libs.test import RestTestCase, UserFactory


class TestTokenView(RestTestCase):

    def setUp(self) -> None:
        raw_password = 'babibbbbbeeeuuee2333'

        self.user = RestTestCase.create_user()
        self.user.set_password(raw_password)
        self.user.save()

        self.email_password = {
            'email'   : self.user.email,
            'password': raw_password
        }

    def test_token_pair_view(self):
        uri = reverse('token_obtain_pair')
        response = self.client.post(path=uri, data=dict(self.email_password))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_pair_failed_not_active_user(self):
        raw_password = 'babibbbbbeeeuuee2333'

        user = RestTestCase.create_user(is_active=False)
        user.set_password(raw_password)
        user.save()
        email_password = {
            'email'   : user.email,
            'password': raw_password
        }

        uri = reverse('token_obtain_pair')
        response = self.client.post(path=uri, data=email_password)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_response_body_token_pair_view(self):
        uri = reverse('token_obtain_pair')
        response = self.client.post(path=uri, data=dict(self.email_password))

        for k in ('refresh', 'access', 'user'):
            self.assertIsNotNone(response.data.get(k))

    def test_token_refresh_view(self):
        uri_token = reverse('token_obtain_pair')
        resp_login = self.client.post(path=uri_token, data=dict(self.email_password))

        token_refr = resp_login.data.get('refresh')
        uri_refresh = reverse('token_refresh')
        response = self.client.post(path=uri_refresh, data={
            'refresh': token_refr
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsNotNone(response.data.get('access'))
        self.assertIsInstance(response.data.get('access'), str)
        self.assertIsNone(response.data.get('refresh'))


class TestUserCreateView(RestTestCase):

    def setUp(self) -> None:
        super().setUp()
        # turn off throttle scope so we dont get 429 after certain tests
        from atlas.api.v1.views.account import UserCreateView
        UserCreateView.throttle_scope = None

    @patch('atlas.apps.account.signals.redis.enqueue')
    def test_register_user_with_npm(self, mock_enqueue):
        data = {
            'email'              : 'wisnu1c@csui.com',
            'password'           : 'password123ccc',
            'firstName'          : 'wisnu',
            'lastName'           : 'pramadhitya',
            'birthdate'          : '1998-01-14',
            'latestCsuiProgram'  : 'S1-IK',
            'latestCsuiClassYear': 2016,
            'uiSsoNpm'           : '1606918059'
        }

        uri = reverse('account_register')
        response = self.client.post(path=uri, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for k in ('refresh', 'access', 'user'):
            self.assertIsNotNone(response.data.get(k))

        resp_data = json.loads(response.content)
        self.assertEqual(resp_data.get('user').get('profile').get('profilePicUrl'),
                         'https://alumni-prod.s3-ap-southeast-1.amazonaws.com/img/default-profile-pic.jpeg')

        mock_enqueue.assert_called()

    @patch('atlas.apps.account.signals.redis.enqueue')
    def test_register_user_without_npm(self, mock_enqueue):
        data = {
            'email'              : 'wisnu1c@csui.com',
            'password'           : 'password123ccc',
            'firstName'          : 'wisnu',
            'lastName'           : 'pramadhitya',
            'birthdate'          : '1998-01-14',
            'latestCsuiProgram'  : 'S1-IK',
            'latestCsuiClassYear': 2016,
        }

        uri = reverse('account_register')
        response = self.client.post(path=uri, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for k in ('refresh', 'access', 'user'):
            self.assertIsNotNone(response.data.get(k))

        mock_enqueue.assert_called()

    # @patch('atlas.apps.account.signals.redis.enqueue')
    # def test_register_user_npm_numeric(self, mock_enqueue):
    #     data = {
    #         'email'              : 'wisnu1c@csui.com',
    #         'password'           : 'password123ccc',
    #         'firstName'          : 'wisnu',
    #         'lastName'           : 'pramadhitya',
    #         'birthdate'          : '1998-01-14',
    #         'latestCsuiProgram'  : 'S1-IK',
    #         'latestCsuiClassYear': 2016,
    #         'uiSsoNpm'           : '16069xx05x'
    #     }
    #
    #     uri = reverse('account_register')
    #     response = self.client.post(path=uri, data=data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    #     # response data is in pythonic
    #     self.assertTrue('uiSsoNpm' in json.loads(response.content))

    @patch('atlas.apps.account.signals.redis.enqueue')
    def test_register_user_npm_unique_if_is_verified(self, mock_enqueue):
        TestUserCreateView.create_user(ui_sso_npm='1606918055', is_verified=True)
        data = {
            'email'              : 'wisnu1c@csui.com',
            'password'           : 'password123ccc',
            'firstName'          : 'wisnu',
            'lastName'           : 'pramadhitya',
            'birthdate'          : '1998-01-14',
            'latestCsuiProgram'  : 'S1-IK',
            'latestCsuiClassYear': 2016,
            'uiSsoNpm'           : '1606918055'
        }

        uri = reverse('account_register')
        response = self.client.post(path=uri, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # response data is in pythonic
        self.assertTrue('uiSsoNpm' in json.loads(response.content))

    @patch('atlas.apps.account.signals.redis.enqueue')
    def test_register_user_low_quality_password(self, mock_enqueue):
        data = {
            'email'              : 'wisnu1c@csui.com',
            'password'           : 'abcde123',
            'firstName'          : 'wisnu',
            'lastName'           : 'pramadhitya',
            'birthdate'          : '1998-01-14',
            'latestCsuiProgram'  : 'S1-IK',
            'latestCsuiClassYear': 2016,
        }

        uri = reverse('account_register')
        response = self.client.post(path=uri, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # response data is in pythonic
        self.assertTrue('nonFieldErrors' in json.loads(response.content))

    @patch('atlas.apps.account.signals.redis.enqueue')
    def test_register_user_class_year_not_greater_than_today(self, mock_enqueue):
        data = {
            'email'              : 'wisnu1c@csui.com',
            'password'           : 'awd1aw1da3wd45a4',
            'firstName'          : 'wisnu',
            'lastName'           : 'pramadhitya',
            'birthdate'          : '1998-01-14',
            'latestCsuiProgram'  : 'S1-IK',
            'latestCsuiClassYear': (timezone.now() + timezone.timedelta(days=365 + 31)).year,
        }

        uri = reverse('account_register')
        response = self.client.post(path=uri, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # response data is in pythonic
        self.assertTrue('latestCsuiClassYear' in json.loads(response.content))

    @patch('atlas.apps.account.signals.redis.enqueue')
    def test_register_user_class_year_not_less_than_1986(self, mock_enqueue):
        data = {
            'email'              : 'wisnu1c@csui.com',
            'password'           : 'awd1aw1da3wd45a4',
            'firstName'          : 'wisnu',
            'lastName'           : 'pramadhitya',
            'birthdate'          : '1998-01-14',
            'latestCsuiProgram'  : 'S1-IK',
            'latestCsuiClassYear': 1984,
        }

        uri = reverse('account_register')
        response = self.client.post(path=uri, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # response data is in pythonic
        self.assertTrue('latestCsuiClassYear' in json.loads(response.content))

    @patch('atlas.apps.account.signals.redis.enqueue')
    def test_register_user_email_is_unique(self, mock_enqueue):
        TestUserCreateView.create_user(email='wisnu1c@csui.com')
        data = {
            'email'              : 'wisnu1c@csui.com',
            'password'           : 'adwawdbbb23123131',
            'firstName'          : 'wisnu',
            'lastName'           : 'pramadhitya',
            'birthdate'          : '1998-01-14',
            'latestCsuiProgram'  : 'S1-IK',
            'latestCsuiClassYear': 2016,
        }

        uri = reverse('account_register')
        response = self.client.post(path=uri, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # response data is in pythonic
        self.assertTrue('email' in json.loads(response.content))


class TestUserDetailView(RestTestCase):

    def setUp(self) -> None:
        super().setUp()
        len_user = 5
        self.users_verified = UserFactory.build_batch(len_user, is_verified=True)
        self.users_unverified = UserFactory.build_batch(len_user, is_verified=False)
        self.users_inactive = UserFactory.build_batch(len_user, is_active=False)

        for i in range(len_user):
            self.users_verified[i].save()
            self.users_unverified[i].save()
            self.users_inactive[i].save()

        raw_password = 'babibbbbbeeeuuee2333'
        self.user = RestTestCase.create_user()
        self.user.set_password(raw_password)
        self.user.save()

        self.email_password = {
            'email'   : self.user.email,
            'password': raw_password
        }

    def test_retrieve_user(self):
        self.authenticate(self.user)
        self.user.is_verified = True
        self.user.save()

        target_user = self.users_verified[random.randint(0, len(self.users_verified) - 1)]
        uri = reverse('account_user_detail', kwargs={'pk': target_user.id})
        response = self.client.get(uri)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        fields = (
            'id',
            'name',
            'firstName',
            'lastName',
            'email',
            'username',
            'uiSsoNpm',
            'groups',
            'lastLogin',
            'isVerified',
            'isActive',
            'isStaff',
            'isSuperuser',
            'isVerified',
            'profile',
        )

        data = json.loads(response.content)
        for f in fields:
            self.assertIn(f, data)

        self.assertEqual(data.get('id'), str(getattr(target_user, 'id')))
        self.logout()

    def test_retrieve_user_not_found(self):
        self.authenticate(self.user)
        self.user.is_verified = True
        self.user.save()

        uri = reverse('account_user_detail', kwargs={'pk': 'hehehe'})
        response = self.client.get(uri)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.logout()

    def test_not_authorized_retrieve_user(self):
        self.logout()
        target_user = self.users_verified[random.randint(0, len(self.users_verified) - 1)]
        uri = reverse('account_user_detail', kwargs={'pk': target_user.id})
        response = self.client.get(uri)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unverified_user_retrieve_other_user(self):
        self.authenticate(self.user)
        self.user.is_verified = False
        self.user.save()

        target_user = self.users_verified[random.randint(0, len(self.users_verified) - 1)]
        uri = reverse('account_user_detail', kwargs={'pk': target_user.id})
        response = self.client.get(uri)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.logout()

    def test_unverified_user_retrieve_self(self):
        self.authenticate(self.user)
        self.user.is_verified = False
        self.user.save()

        uri = reverse('account_user_detail', kwargs={'pk': self.user.id})
        response = self.client.get(uri)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logout()

    def test_user_retrieve_inactive(self):
        self.authenticate(self.user)
        self.user.is_verified = False
        self.user.save()

        target_user = self.users_inactive[random.randint(0, len(self.users_inactive) - 1)]
        uri = reverse('account_user_detail', kwargs={'pk': target_user.id})
        response = self.client.get(uri)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.logout()

    def test_user_retrieve_unverified(self):
        self.authenticate(self.user)
        self.user.is_verified = True
        self.user.save()

        target_user = self.users_unverified[random.randint(0, len(self.users_unverified) - 1)]
        uri = reverse('account_user_detail', kwargs={'pk': target_user.id})
        response = self.client.get(uri)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logout()

    @patch('atlas.apps.account.signals.redis.enqueue')
    def test_user_update_unauthorized(self, mock_enqueue):
        self.user.is_verified = True
        self.user.save()

        uri = reverse('account_user_detail', kwargs={'pk': self.user.id})
        response = self.client.patch(uri)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(uri)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('atlas.apps.account.signals.redis.enqueue')
    def test_user_update_patch_self(self, mock_enqueue):
        self.authenticate(self.user)
        self.user.is_verified = False
        self.user.save()

        # neutralize from .save()
        mock_enqueue.reset_mock()

        user_data = {
            'firstName': 'trapolin',
            'lastName' : 'lapolin',
            'profile'  : {
                'gender'             : 'M',
                'residence_city'     : 'Surabaya',
                'birthdate'          : '1998-01-14',
                'latestCsuiProgram'  : 'S1-SI',
                'latestCsuiClassYear': 2010,
            }
        }

        uri = reverse('account_user_detail', kwargs={'pk': self.user.id})
        response = self.client.patch(uri, data=json.dumps(user_data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fields = (
            'id',
            'name',
            'firstName',
            'lastName',
            'email',
            'username',
            'uiSsoNpm',
            'groups',
            'lastLogin',
            'isVerified',
            'isActive',
            'isStaff',
            'isSuperuser',
            'isVerified',
            'profile',
        )
        data = json.loads(response.content)
        for f in fields:
            self.assertIn(f, data)

        profile_fields = (
            'dateCreated',
            'dateUpdated',
            'gender',
            'phoneNumber',
            'birthdate',
            'residenceCity',
            'residenceCountry',
            'residenceLng',
            'residenceLat',
            'latestCsuiClassYear',
            'latestCsuiProgram',
            'profilePicUrl',
            'websiteUrl',
        )

        for f in profile_fields:
            self.assertIn(f, data.get('profile'))

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'trapolin')
        self.assertEqual(self.user.last_name, 'lapolin')
        self.assertIsNone(self.user.ui_sso_npm)
        self.assertEqual(self.user.profile.gender, 'M')
        self.assertEqual(self.user.profile.residence_city, 'Surabaya')
        self.assertEqual(str(self.user.profile.birthdate), '1998-01-14')
        self.assertEqual(self.user.profile.latest_csui_program, 'S1-SI')
        self.assertEqual(self.user.profile.latest_csui_class_year, 2010)

        mock_enqueue.assert_called()

    @patch('atlas.apps.account.signals.redis.enqueue')
    def test_user_update_patch_self_npm_null_or_something(self, mock_enqueue):
        self.authenticate(self.user)
        self.user.is_verified = False
        self.user.save()

        # neutralize from .save()
        mock_enqueue.reset_mock()

        user_data = {
            'firstName': 'trapolin',
            'lastName' : 'lapolin',
            'uiSsoNpm': None,
        }

        uri = reverse('account_user_detail', kwargs={'pk': self.user.id})
        response = self.client.patch(uri, data=json.dumps(user_data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('atlas.apps.account.signals.redis.enqueue')
    def test_user_update_put_self(self, mock_enqueue):
        self.authenticate(self.user)
        self.user.is_verified = False
        self.user.save()

        # neutralize from .save()
        mock_enqueue.reset_mock()

        user_data = {
            'firstName': 'trapolin',
            'lastName' : 'lapolin',
            'uiSsoNpm' : '1606918233',
            'profile'  : {
                'gender'             : 'M',
                'residence_city'     : 'Surabaya',
                'birthdate'          : '1998-01-14',
                'latestCsuiProgram'  : 'S1-SI',
                'latestCsuiClassYear': 2010,
            }
        }

        uri = reverse('account_user_detail', kwargs={'pk': self.user.id})
        response = self.client.put(uri, data=json.dumps(user_data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fields = (
            'id',
            'name',
            'firstName',
            'lastName',
            'email',
            'username',
            'uiSsoNpm',
            'groups',
            'lastLogin',
            'isVerified',
            'isActive',
            'isStaff',
            'isSuperuser',
            'isVerified',
            'profile',
        )
        data = json.loads(response.content)
        for f in fields:
            self.assertIn(f, data)

        profile_fields = (
            'dateCreated',
            'dateUpdated',
            'gender',
            'phoneNumber',
            'birthdate',
            'residenceCity',
            'residenceCountry',
            'residenceLng',
            'residenceLat',
            'latestCsuiClassYear',
            'latestCsuiProgram',
            'profilePicUrl',
            'websiteUrl',
        )

        for f in profile_fields:
            self.assertIn(f, data.get('profile'))

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'trapolin')
        self.assertEqual(self.user.last_name, 'lapolin')
        self.assertEqual(self.user.ui_sso_npm, '1606918233')
        self.assertEqual(self.user.profile.gender, 'M')
        self.assertEqual(self.user.profile.residence_city, 'Surabaya')
        self.assertEqual(str(self.user.profile.birthdate), '1998-01-14')
        self.assertEqual(self.user.profile.latest_csui_program, 'S1-SI')
        self.assertEqual(self.user.profile.latest_csui_class_year, 2010)

        mock_enqueue.assert_called()

    @patch('atlas.apps.account.signals.redis.enqueue')
    def test_user_verified_update_self(self, mock_enqueue):
        self.authenticate(self.user)
        self.user.is_verified = True
        self.user.save()

        mock_enqueue.reset_mock()

        user_data = {
            'firstName': 'trapolin',
            'lastName' : 'lapolin',
            'uiSsoNpm' : '1606918233',
            'profile'  : {
                'gender'             : 'M',
                'residence_city'     : 'Surabaya',
                'birthdate'          : '1998-01-14',
                'latestCsuiProgram'  : 'S1-SI',
                'latestCsuiClassYear': 2010,
            }
        }

        uri = reverse('account_user_detail', kwargs={'pk': self.user.id})
        self.client.patch(uri, data=json.dumps(user_data), content_type='application/json')

        self.user.refresh_from_db()
        self.assertNotEqual(self.user.first_name, 'trapolin')
        self.assertNotEqual(self.user.last_name, 'lapolin')
        self.assertNotEqual(self.user.ui_sso_npm, '1606918233')
        self.assertNotEqual(str(self.user.profile.birthdate), '1998-01-14')
        self.assertNotEqual(self.user.profile.latest_csui_program, 'S1-SI')
        self.assertNotEqual(self.user.profile.latest_csui_class_year, 2010)

        self.assertEqual(self.user.profile.gender, 'M')
        self.assertEqual(self.user.profile.residence_city, 'Surabaya')

        mock_enqueue.assert_called_once()

    @patch('atlas.apps.account.signals.redis.enqueue')
    def test_user_update_other_user(self, mock_enqueue):
        self.authenticate(self.user)
        self.user.is_verified = True
        self.user.save()

        target_user = self.users_unverified[random.randint(0, len(self.users_unverified) - 1)]
        uri = reverse('account_user_detail', kwargs={'pk': target_user.id})
        response = self.client.patch(uri)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        target_user = self.users_inactive[random.randint(0, len(self.users_inactive) - 1)]
        uri = reverse('account_user_detail', kwargs={'pk': target_user.id})
        response = self.client.patch(uri)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
