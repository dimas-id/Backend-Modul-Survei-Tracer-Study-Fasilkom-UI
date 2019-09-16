from atlas.libs.client import AbstractClient, AbstractClientManager

from django.conf import settings

LINKEDIN_CLIENT_ID = settings.LINKEDIN_CLIENT_ID
LINKEDIN_CLIENT_SECRET = settings.LINKEDIN_CLIENT_SECRET


class OAuth2LinkedinClient(AbstractClient):
    max_retry_attempt = 0

    class Meta:
        always_use_production = True
        is_camelized = False
        client_url = {
            'production': 'https://www.linkedin.com/oauth',
            'development': ''
        }


class LinkedinOAuth2Manager(AbstractClientManager):
    client = OAuth2LinkedinClient()

    def request_token(self, code, redirect_uri):
        params = {
            'client_secret': LINKEDIN_CLIENT_SECRET,
            'client_id': LINKEDIN_CLIENT_ID,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
        }
        uri = f'/v2/accessToken?'
        for key in params.keys():
            uri = f'{uri}{key}={params[key]}&'

        self.client.set_header('content_type', 'application/json')
        response = self.client.post(uri)
        self.client.clear_header()
        return response


class LinkedinClient(AbstractClient):
    max_retry_attempt = 0

    def get_headers(self):
        headers = super().get_headers()
        headers['X-RestLi-Protocol-Version'] = '2.0.0'
        return headers

    class Meta:
        always_use_production = True
        is_camelized = True
        client_url = {
            'production': 'https://api.linkedin.com',
            'development': ''
        }


class LinkedinPersonManager(AbstractClientManager):
    client = LinkedinClient()

    def get_email_address(self, access_token):
        uri = '/v2/emailAddress?q=members&projection=(elements*(handle~))'
        self.get_client().set_header('Authorization', f'Bearer {access_token}')
        return self.get_client().get(uri, format='json')

    def get_person_lite_profile(self, access_token):
        uri = "v2/me?projection=(id,firstName,lastName,profilePicture(displayImage~:playableStreams))"
        self.get_client().set_header('Authorization', f'Bearer {access_token}')
        return self.client.get(uri, format='json')
