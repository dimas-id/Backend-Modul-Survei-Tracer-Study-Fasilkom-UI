from django.test import TestCase
from faker import Faker

from atlas.apps.account.models import User
# Create your tests here.


class UserTest(TestCase):

    def setUp(self):
        self.faker = Faker()
        self.user_data = {
            'first_name': self.faker.name(),
            'last_name': self.faker.name(),
            'email': 'balala@admin.com'
        }

    def test_create_user(self):
        user = User.objects.create_user('hello123', **self.user_data)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_verified)
        self.assertFalse(user.is_email_verified)
        self.assertFalse(user.is_paired_sso)

        self.assertEqual(
            user.name, f'{self.user_data["first_name"]} {self.user_data["last_name"]}')

        user.set_as_verified()
        self.assertTrue(User.objects.get(id=user.id).is_verified)

    def test_create_superuser(self):
        user = User.objects.create_superuser('hello123', **self.user_data)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_username_is_unique(self):
        user1 = User.objects.create_user('hello123', **self.user_data)

        user_data2 = dict(self.user_data)
        user_data2['email'] = 'hehe@hee.com'
        user2 = User.objects.create_user('hello123', **user_data2)

        self.assertNotEqual(user1.username, user2.username)

    def test_username_is_not_updated_by_name(self):
        user1 = User.objects.create_user('hello123', **self.user_data)
        old_username = user1.username
        user1.first_name = 'john'
        user1.last_name = 'doe'

        # username must not update
        self.assertEqual(user1.username, old_username)

    def test_create_user_profile(self):
        user = User.objects.create_user('hello123', **self.user_data)
        # check signal
        self.assertIsNotNone(user.profile)
        self.assertIsNotNone(user.profile.profile_pic_url)
