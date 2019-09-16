
import os
import requests
import json

from django.conf import settings
from django.contrib.auth import login as auth_login
from django.http import (
    HttpResponseRedirect,
    HttpResponse,
)

from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response

from atlas.apps.external_auth.utils import (
    LinkedinHelper,
)
from atlas.apps.external_auth.services import ExternalAuthService
from atlas.clients.linkedin.api import (
    LinkedinOAuth2Manager,
    LinkedinPersonManager
)


class LinkedinRequestAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        helper = LinkedinHelper()
        request.session['external_auth_state'] = helper.get_random_state()
        return HttpResponseRedirect(
            helper.get_oauth2_url(request.session['external_auth_state']))


class LinkedinCallbackAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        helper = LinkedinHelper()
        REDIRECT_URL = helper.get_redirect_url()
        error = request.GET.get('error', '')
        if error != '':
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

        state = request.GET.get('state', '')
        if state != request.session.get('external_auth_state'):
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)

        code = request.GET.get('code', '')
        response_data, auth_success, _ = LinkedinOAuth2Manager().request_token(code,
                                                                            REDIRECT_URL)
        user_data, person_success, _ = LinkedinPersonManager().get_person_basic_profile(
            response_data.get('access_token'))

        user = None
        created = False
        if auth_success and person_success:
            user, created = ExternalAuthService().get_or_register_linkedin_user(**user_data)
            # make user is authenticated
            auth_login(request, user)

        return helper.redirect_to_frontend(user, created)
