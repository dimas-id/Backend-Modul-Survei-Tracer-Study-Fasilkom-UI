from datetime import date

from django.db import transaction

from atlas.apps.account.constants import C_UI_PROGRAMS_FIELD, C_UI_STATUS, C_UI_NAME_FIELD
from atlas.apps.experience.utils import check_verified_status
from atlas.clients.csui import StudentManager
from atlas.clients.elastic import ElasticManager
from .models import Position, Education
from atlas.apps.experience.utils import (
    validate_alumni_data, extract_alumni_data, get_most_matching_mahasiswa)


class ExperienceService:

    def extract_and_create_positions_from_linkedin(self, user, positions):
        list_pos = []

        # linkedin is not providing day
        def transform_date(dict_date): return date(
            dict_date['year'], dict_date['month'], 1)

        for pos in positions:
            location = pos['location'].get('name')

            date_ended = None
            if not pos['is_current']:
                date_ended = transform_date(pos['end_date'])

            date_started = transform_date(pos['start_date'])
            new_pos = Position.objects.create(
                user=user,
                title=pos['title'],
                company_name=pos['company']['name'],
                industry_name=pos['company']['industry'],
                location_name=location,
                date_ended=date_ended,
                date_started=date_started,
                company_metadata=pos['company'])

            list_pos.append(new_pos)

        return list_pos

    @transaction.atomic
    def verify_user_registration(self, education: Education):
        """
        Verify user registration data.
        It will run async and must, the reason is
        * it could get longer time to request to csui server
        * we need to requests mahasiswa list by class year if user forget the npm
          then we need to iterate all O(N) and find the right user.
        * because latency
        """

        is_siak = (education.csui_program[:2] == "S2" and education.csui_class_year > 2004) or \
                  (education.csui_program[:2] == "S1" and education.csui_class_year > 2001)

        student_manager = StudentManager() if is_siak else ElasticManager()

        user_npm = getattr(education, 'ui_sso_npm', None)
        mahasiswa_data = None
        if user_npm is not None and user_npm.strip() != '':
            print(user_npm)
            mahasiswa_data, success, _ = student_manager.get_student_by_npm(user_npm)
        else:
            # how if the api is using paginator? LOL
            user_fullname = [getattr(education.user, 'first_name'), getattr(education.user, 'last_name', None)]
            user_fullname_concat = getattr(education.user, 'name')
            mahasiswa_list = []
            if is_siak:
                for name in user_fullname:
                    if name and name.strip():
                        mahasiswa_list_temp, success, _ = student_manager.get_students_by_name(
                            name)
                        mahasiswa_list.extend(mahasiswa_list_temp)
            else:
                mahasiswa_list, success = student_manager.get_students_by_name(user_fullname_concat)
            # we must find the mhs using name
            if success:
                mahasiswa_data, _ = get_most_matching_mahasiswa(
                    mahasiswa_list, user_fullname_concat, lambda mhs_data: mhs_data.get(C_UI_NAME_FIELD), \
                    education.csui_program[:2])
        is_valid = False
        if mahasiswa_data is not None and success:
            # not none then we validatez
            try:
                data = extract_alumni_data(mahasiswa_data,education.csui_program[:2])
                is_valid = validate_alumni_data(education, *data)
            except Exception as e:
                is_valid = False

            if is_valid:
                education.set_as_verified
                setattr(education, 'ui_sso_npm', data[1])
                setattr(education.user.profile, 'birthdate', data[2])
                setattr(education, 'csui_program', data[3])
                setattr(education, 'csui_class_year', data[4])

                # get latest status, the default i think is Kosong in CSUI API
                latest_status = mahasiswa_data.get(C_UI_PROGRAMS_FIELD)[0].get(
                    C_UI_STATUS) if len(mahasiswa_data.get(C_UI_PROGRAMS_FIELD)) > 0 else 'Kosong'
                setattr(education, 'csui_graduation_status',
                        latest_status)
                if Education.objects.filter(id=education.id).exists():
                    education.user.profile.save(update_fields=('birthdate',))
                    education.save(update_fields=('ui_sso_npm','csui_program','csui_class_year','csui_graduation_status'))
        #Change user verification status
        check_verified_status(education.user)

        return is_valid, mahasiswa_data