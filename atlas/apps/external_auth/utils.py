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
            "scope=r_basicprofile r_emailaddress rw_company_admin w_share"
        )

    def get_random_state(self):
        random_state = ''.join(
            [random.choice(
                string.ascii_letters + string.digits
            ) for n in range(32)]
        )
        return random_state

    def redirect_to_frontend(self, user=None):
        redirect_url = f'{settings.FRONTEND_URL}/register-external-auths'
        if user is None:
            redirect_url = f'{settings.FRONTEND_URL}/error'

        response = HttpResponseRedirect(redirect_url)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            expire_at = timezone.now() + timezone.timedelta(days=1)

            # @todo secure domain, secure cookies & max age
            response.set_cookie('user_id', user.id)
            response.set_cookie('access', str(
                refresh.access_token),  expires=expire_at)
            response.set_cookie('refresh', str(refresh),
                                expires=expire_at)
        return response
