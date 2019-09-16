import random
import string
import json

from django.conf import settings
from django.http import (
    HttpResponseRedirect,
)
from django.utils import timezone
from django.urls import reverse

from rest_framework_simplejwt.tokens import RefreshToken


class LinkedinHelper:

    def get_redirect_url(self):
        return settings.DEPLOYMENT_ROOT_URL + \
            reverse('external_auth_linkedin_callback')

    def get_oauth2_url(self, state):
        CLIENT_ID_LINKEDIN = settings.LINKEDIN_CLIENT_ID
        REDIRECT_URI = self.get_redirect_url()
        return (
            "https://www.linkedin.com/oauth/v2/authorization?" +
            "response_type=code&" +
            "client_id=" + CLIENT_ID_LINKEDIN + "&" +
            "redirect_uri=" + REDIRECT_URI + "&" +
            "state=" + state + "&" +
            "scope=r_emailaddress r_liteprofile"
        )

    def get_random_state(self):
        random_state = ''.join(
            [random.choice(
                string.ascii_letters + string.digits
            ) for n in range(32)]
        )
        return random_state

    def redirect_to_frontend(self, user, new_user: bool):
        redirect_url = f'{settings.FRONTEND_URL}/register-external-auths'
        if user is None:
            redirect_url = f'{settings.FRONTEND_URL}/err'

        response = HttpResponseRedirect(redirect_url)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            expire_at = timezone.now() + timezone.timedelta(days=1)

            domain = settings.FRONTEND_URI

            # @todo secure domain, secure cookies & max age
            response.set_cookie('user_id', user.id, domain=domain)
            response.set_cookie('access', str(
                refresh.access_token),  expires=expire_at, domain=domain)
            response.set_cookie('refresh', str(refresh),
                                expires=expire_at, domain=domain)
            response.set_cookie(
                'should_complete_registration', json.dumps(new_user), domain=domain)
        return response


def extract_email_and_profile_from_linkedin_response(email_data:dict, profile_data:dict):
    user = {}
    user['email_address'] = email_data['elements'][0]['handle~']
    user['id'] = profile_data['id']
    user['first_name'] = profile_data['firstName']['localized']['en_US']
    user['first_name'] = profile_data['lastName']['localized']['en_US']

    try:
        # less priority
        dp = profile_data['profilePicture']['displayImage~']
        last_dp = dp['paging']['count'] - 1
        user['picture_url'] = dp['elements'][last_dp]['identifiers']['identifier']
    except:
        pass

    return user
