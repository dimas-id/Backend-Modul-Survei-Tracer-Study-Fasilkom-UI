from atlas.libs.client import AbstractClient, AbstractClientManager

from django.conf import settings

LINKEDIN_CLIENT_ID = settings.LINKEDIN_CLIENT_ID
LINKEDIN_CLIENT_SECRET = settings.LINKEDIN_CLIENT_SECRET


class OAuth2LinkedinClient(AbstractClient):
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
    class Meta:
        always_use_production = True
        is_camelized = True
        client_url = {
            'production': 'https://api.linkedin.com',
            'development': ''
        }


class LinkedinPersonManager(AbstractClientManager):
    client = LinkedinClient()

    def get_person_basic_profile(self, access_token):
        scope = (
            "id,first-name,last-name,headline,location,industry,"
            "current-share,num-connections,summary,specialties,"
            "positions,picture-url,public-profile-url,email-address,"
            "api-standard-profile-request"
        )
        uri = "/v1/people/~:({})?".format(scope)
        return self.client.get(uri, oauth2_access_token=access_token, client_id=LINKEDIN_CLIENT_ID, format='json')
