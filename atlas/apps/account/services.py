
from datetime import date

from django.db import (transaction, IntegrityError)
from django.contrib.auth import (
    get_user_model, password_validation)
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _

from rest_framework.authentication import authenticate

User = get_user_model()


class AuthService:
    username_field = User.USERNAME_FIELD

    def __init__(self, *args, **kwags):
        pass

    @transaction.atomic
    def registerPublicUser(self, request: HttpRequest, identifier: str, password: str,
                           first_name: str, last_name: str, ui_sso_npm: str = None, **profile):
        """
        Registration procedure for public user (alumnus, student, and
        who want to join as member).
        Using redis-queue, We will validate the data (npm, angkatan,
        birthdate, and others) to UI academic service.
        For alumnus under 2004, we must validate them manually
        by checking to database provided by client.
        """

        # for now just register the user
        user = User.objects.create_user(
            password=password, email=identifier, first_name=first_name,
            last_name=last_name, ui_sso_npm=ui_sso_npm)
            # user = authenticate(request, **{self.username_field: getattr(user,
            #                                                       self.username_field), 'password': password})

        for attr in profile:
            setattr(user.profile, attr, profile[attr])
        user.profile.save()

        return user
