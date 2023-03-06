from django.contrib.auth import (
    get_user_model)
from django.db import (transaction)
from django.http import HttpRequest

from atlas.clients.csui.api import StudentManager, GraduatedStudentManager
from atlas.apps.account.utils import generate_random_password

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
    def register_public_bulk_user(self, request: HttpRequest, identifier: str, first_name: str,
                             last_name: str, ui_sso_npm: str = None, **profile):
        """
        Registration procedure for bulk user (alumnus, student, and
        who want to join as member).
        """

        password = generate_random_password()
        print("password : " + password)
        # for now just register the user
        user = User.objects.create_user(
                password=password, first_name=first_name,
                last_name=last_name, ui_sso_npm=ui_sso_npm, 
                is_from_sisidang=True, **{self.Meta.username_field: identifier})

        for attr in profile:
            setattr(user.profile, attr, profile[attr])
        user.profile.save()
        return user
    
    def map_sisidang_response(self, tahun, term):
        alumni_manager = GraduatedStudentManager()
        periode = tahun + "/" + str(int(tahun) + 1)
        alumni_data, success, _ = alumni_manager.get_all_student_by_year_and_term(periode, term)

        final_request = []
        ind_object = {
            "birthdate": "",
            "email": "",
            "first_name": "",
            "last_name": "",
            "linkedin_url": "",
            "phone_number": "",
            "residence_country" : "",
            "education": {
                "csui_class_year": "",
                "csui_program": "",
                "ui_sso_npm": ""
            },
            "position": {
                "company_name": "",
                "date_ended": "",
                "date_started": "",
                "industry_name": "",
                "location_name": "",
                "title": "",
                "is_from_sisidang": ""
            }
        }

        if alumni_data is not None and success:
            for alumni in alumni_data:
                cop_obj = ind_object.copy()
                cop_obj["birthdate"] = alumni.get("tanggal_lahir")
                cop_obj["email"] = alumni.get("email")

                try:
                    nama = alumni.get("nama").split(" ", 1)
                    cop_obj["first_name"] = nama[0]
                    cop_obj["last_name"] = nama[1]
                except:
                    cop_obj["first_name"] = alumni.get("nama")
                    cop_obj["last_name"] = alumni.get("nama")

                if alumni.get("linkedin") == "-":
                    cop_obj.pop("linkedin_url")
                elif "https://" not in alumni.get("linkedin"):
                    cop_obj["linkedin_url"] = "https://" + alumni.get("linkedin")
                else:
                    cop_obj["linkedin_url"] = alumni.get("linkedin")
                    
                cop_obj["phone_number"] = alumni.get("kontak").get("whatsapp")
                cop_obj["residence_country"] = alumni.get("domisili")

                edu_obj = cop_obj["education"].copy()

                edu_obj["csui_class_year"] = alumni.get("angkatan")

                switcher = {
                    1: "S1-IK",
                    2: "S1-IK",
                    3: "S1_KI-IK",
                    4: "S1-SI",
                    5: "S1-SI",
                    6: "S1_EKS-SI",
                    7: "S2-IK",
                    8: "S2-TI",
                    9: "S3-IK"
                }
                edu_obj["csui_program"] = switcher.get(alumni.get("prodi"))
                edu_obj["ui_sso_npm"] = alumni.get("npm")

                cop_obj["education"] = edu_obj

                pos_obj = cop_obj["position"].copy()

                if alumni.get("pekerjaan").get("posisi") != "Mahasiswa":
                    pos_obj["company_name"] = alumni.get("pekerjaan").get("perusahaan")
                    pos_obj["date_ended"] = alumni.get("pekerjaan").get("tanggal_selesai")
                    pos_obj["date_started"] = alumni.get("pekerjaan").get("tanggal_mulai")
                    pos_obj["industry_name"] = alumni.get("pekerjaan").get("industri")
                    pos_obj["location_name"] = alumni.get("pekerjaan").get("lokasi")
                    pos_obj["title"] = alumni.get("pekerjaan").get("posisi")
                    pos_obj["is_from_sisidang"] = True

                cop_obj["position"] = pos_obj

                final_request.append(cop_obj.copy())
        
        return final_request
