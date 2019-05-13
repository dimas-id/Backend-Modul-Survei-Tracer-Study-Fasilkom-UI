from django.conf import settings
from atlas.libs.client import AbstractClient, UserManagerAdapter
from atlas.libs.dataclass import DataClass


class UserDC(DataClass):
    class Meta:
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'preference',
            'groups',
            'is_verified',
            'is_active',
            'is_staff',
            'is_superuser',
        )


class HeliosClient(AbstractClient):

    class Meta:
        always_use_production = False
        is_camelized = True
        client_url = {
            'production' : f'https://{settings.HELIOS_URI}/api/v1',
            'development': 'http://localhost:8004/api/v1'
        }


class UserHeliosManager(UserManagerAdapter):
    client = HeliosClient()

    def set_authorization(self):
        self.get_client().set_header('authorization', f'Signature {settings.API_KEY}')

    def update_or_create_user(self, user_id: str, user):
        uri = f'/users/{user_id}'
        self.set_authorization()
        response = self.get_client().put(uri=uri, data=UserDC.from_object(obj=user).to_dict())
        self.get_client().clear_header()
        return response
