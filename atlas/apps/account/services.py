from datetime import date

from django.db import (transaction, IntegrityError)
from django.contrib.auth import (
    get_user_model, password_validation)
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _

from rest_framework.authentication import authenticate

from atlas.clients.csui.api import StudentManager
# from atlas.apps.account.utils import validate_alumni_data, extract_alumni_data

User = get_user_model()


class UserService:

    student_manager = StudentManager()

    class Meta:
        username_field = User.USERNAME_FIELD
        minimum_score = 65

    @transaction.atomic
    def register_public_user(self, request: HttpRequest, identifier: str, password: str,
                           first_name: str, last_name: str, ui_sso_npm: str = None, **profile):
        """
        Registration procedure for public user (alumnus, student, and
        who want to join as member).
        """

        # for now just register the user
        user = User.objects.create_user(
            password=password, first_name=first_name,
            last_name=last_name, ui_sso_npm=ui_sso_npm,
            **{self.Meta.username_field: identifier})

        for attr in profile:
            setattr(user.profile, attr, profile[attr])
        user.profile.save()
        return user

    def get_or_register_external_auth_user(self, email, first_name, last_name, picture_url):
        try:
            created = False
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            created = True
            user = User.objects.create_user_unusable_password(
                email=email, first_name=first_name, last_name=last_name)

        user.profile.profile_picture_url = picture_url
        user.profile.save(update_fields=('profile_pic_url',))
        return user, created

    def verify_user_registration(self, user: User):
        """
        Verify user registration data.
        It will run async and must, the reason is
        * it could get longer time to request to csui server
        * we need to requests mahasiswa list by class year if user forget the npm
          then we need to iterate all O(N) and find the right user.
        * because latency
        """
        user_npm = getattr(user, 'ui_sso_npm', None)
        mahasiswa_data = None
        # if user_npm is not None:
        #     mahasiswa_data, success = self.student_manager.get_student_by_npm(
        #         user_npm)
        #     # check npm
        #     if success:
        #         # validate alumni
        #         data = extract_alumni_data(mahasiswa_data)
        #         is_valid = validate_alumni_data(user, *data)
        #         if is_valid:
        #             user.set_as_verified()

        # else:
        #     # how if the api is using paginator? LOL
        #     # mahasiswa_list, success = self.student_manager.get_students_by_class(
        #         # csui_class)
        #     # we must find the mhs using name
        #     pass


        # just set verifier
        user.set_as_verified()
