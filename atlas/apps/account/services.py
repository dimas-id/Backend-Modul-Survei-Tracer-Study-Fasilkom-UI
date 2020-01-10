from django.contrib.auth import (
    get_user_model)
from django.db import (transaction)
from django.http import HttpRequest

from atlas.clients.csui.api import StudentManager

User = get_user_model()


class UserService:
    student_manager = StudentManager()

    class Meta:
        username_field = User.USERNAME_FIELD

    @transaction.atomic
    def register_public_user(self, request: HttpRequest, identifier: str, password: str, first_name: str,
                             last_name: str, ui_sso_npm: str = None, **profile):
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

        profile = user.profile
        profile.profile_pic_url = picture_url
        profile.save(update_fields=('profile_pic_url',))
        return user, created
