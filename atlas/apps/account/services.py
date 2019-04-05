from datetime import date

from django.db import (transaction, IntegrityError)
from django.contrib.auth import (
    get_user_model, password_validation)
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _

from rest_framework.authentication import authenticate

from atlas.clients.csui.api import StudentManager
from atlas.libs import redis

User = get_user_model()


class UserService:

    student_manager = StudentManager()

    class Meta:
        username_field = User.USERNAME_FIELD
        ui_npm_field = 'npm'
        ui_name_field = 'name'
        ui_birthdate_field = 'birthdate'

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
            password=password, first_name=first_name,
            last_name=last_name, ui_sso_npm=ui_sso_npm,
            **{self.Meta.username_field: identifier})
        # user = authenticate(request, **{self.username_field: getattr(user,
        #                                                       self.username_field), 'password': password})

        for attr in profile:
            setattr(user.profile, attr, profile[attr])
        user.profile.save()

        redis.enqueue(self.verify_user_registration, user=user)

        return user

    def get_or_register_external_auth_user(self, email, first_name, last_name, picture_url):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user_unusable_password(
                email=email, first_name=first_name, last_name=last_name)

        user.profile.profile_picture_url = picture_url
        user.profile.save(update_fields=('profile_pic_url',))
        return user

    def verify_user_registration(self, user: User):
        """
        Verify user registration data.
        We are using scoring for validation and the minimum score is 65:
        npm: 15 points, because it is an optional field
        name: 25 points
            first_name 5 points, last_name: 10 points, full 10
        birthdate: 20 points
        csui_class: 20 points
        csui_program: 20 points

        It will run async and must, the reason is
        * it could get longer time to request to csui server
        * we need to requests mahasiswa list by class year if user forget the npm
          then we need to iterate all O(N) and find the right user.
        """
        # get all field that we need
        # it just matter of preference, i like using getattr sometimes for clarity
        ui_npm = getattr(user, 'ui_sso_npm', None)
        csui_class = getattr(user.profile, 'latest_csui_class', None)
        birthdate = getattr(user.profile, 'birthdate', None)

        validation_score = 0

        mahasiswa_data = None
        if ui_npm:
            mahasiswa_data, is_by_npm_success = self.student_manager.get_student_by_npm(
                ui_npm)
        else:
            # how if the api is using paginator? LOL
            mahasiswa_list, is_by_npm_success = self.student_manager.get_students_by_class(
                csui_class)
            # we must find the mhs using name

        # check npm
        if is_by_npm_success and mahasiswa_data.get('npm') == ui_npm:
            validation_score += 15

        # dummy, just set the user as valid
        user.set_as_verified()
        user.save(update_fields=('is_verified',))
