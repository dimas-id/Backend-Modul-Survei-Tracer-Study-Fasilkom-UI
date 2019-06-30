import factory
from django.contrib.auth import get_user_model
from faker import Faker
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda a: '{0}.{1}@example.com'.format(a.first_name, a.last_name).lower())
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class RestTestCase(APITestCase):

    @staticmethod
    def create_user(**extra) -> User:
        u = UserFactory(**extra)
        u.set_password(RestTestCase.get_password())
        u.save()
        return u

    @staticmethod
    def get_password():
        return 'hellthisispassword12333311'

    @staticmethod
    def create_admin() -> User:
        return RestTestCase.create_user(is_superuser=True, is_staff=True)

    def setUp(self) -> None:
        self.fake = Faker()

    def authenticate(self, user: User):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

    def logout(self):
        self.client.credentials()
        self.client.logout()
