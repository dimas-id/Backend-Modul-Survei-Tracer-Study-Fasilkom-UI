from django.contrib.auth import (
    get_user_model)
from django.db import (transaction)
from django.http import HttpRequest

from atlas.apps.account.constants import (
    C_UI_NAME_FIELD, C_UI_STATUS, C_UI_PROGRAMS_FIELD)
from atlas.apps.account.utils import (
    validate_alumni_data, extract_alumni_data, get_most_matching_mahasiswa)
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

    @transaction.atomic
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
        if user_npm is not None:
            mahasiswa_data, success, _ = self.student_manager.get_student_by_npm(
                    user_npm)
        else:
            # how if the api is using paginator? LOL
            user_fullname = getattr(user, 'name')
            mahasiswa_list, success, _ = self.student_manager.get_students_by_name(
                    user_fullname)
            # we must find the mhs using name
            if success:
                mahasiswa_data, _ = get_most_matching_mahasiswa(
                        mahasiswa_list, user_fullname, lambda mhs_data: mhs_data.get(C_UI_NAME_FIELD))

        is_valid = False
        if mahasiswa_data is not None and success:
            # not none then we validatez
            try:
                data = extract_alumni_data(mahasiswa_data)
                is_valid = validate_alumni_data(user, *data)
            except Exception:
                is_valid = False

            if is_valid:
                user.set_as_verified()
                setattr(user, 'ui_sso_npm', data[1])
                setattr(user.profile, 'birthdate', data[2])
                setattr(user.profile, 'latest_csui_program', data[3])
                setattr(user.profile, 'latest_csui_class_year', data[4])

                # get latest status, the default i think is Kosong in CSUI API
                latest_status = mahasiswa_data.get(C_UI_PROGRAMS_FIELD)[0].get(
                    C_UI_STATUS) if len(mahasiswa_data.get(C_UI_PROGRAMS_FIELD)) > 0 else 'Kosong'
                setattr(user.profile, 'latest_csui_graduation_status',
                        latest_status)

                user.profile.save(update_fields=('birthdate', 'latest_csui_program',
                                                 'latest_csui_class_year', 'latest_csui_graduation_status',))
                user.save(update_fields=('ui_sso_npm',))

        # todo extract education
        # checknya double register

        return is_valid, mahasiswa_data
