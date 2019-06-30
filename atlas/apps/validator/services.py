from rest_framework.exceptions import APIException
from atlas.clients.csui import StudentManager
from atlas.apps.validator.utils import (
    extract_alumni_data,
    get_most_matching_mahasiswa,
    validate_alumni_data
)
from atlas.apps.validator.models import AlumniValidation
from atlas.apps.validator import constants


class AlumniValidatorService:

    student_manager = StudentManager()

    @staticmethod
    def __validate_alumni__(alumni, data, fields):
        is_valid = validate_alumni_data(alumni, data, fields)
        if is_valid:
            alumni = AlumniValidation(**data)
            alumni.set_valid()
            return alumni
        else:
            alumni.set_invalid()

        return alumni

    def validate_alumni_by_npm(self, npm: str, alumni: AlumniValidation, fields: set = None):
        data, success, response = self.student_manager.get_student_by_npm(npm)
        if success:
            extracted_data = extract_alumni_data(data)
            return AlumniValidatorService.__validate_alumni__(alumni, extracted_data, fields)

        if response is not None:
            e = APIException(detail=data)
            e.status_code = response.status_code
            raise e
        raise APIException(detail='Something wrong')

    def validate_alumni_by_nama(self, nama: str,  alumni: AlumniValidation, fields: set):
        mhs_list, success, response = self.student_manager.get_students_by_name(nama)

        if success:
            candidate_data, _ = get_most_matching_mahasiswa(
                mhs_list, nama, lambda data: data.get(constants.C_UI_NAME_FIELD))
            if candidate_data is not None:
                extracted_data = extract_alumni_data(candidate_data)
                return AlumniValidatorService.__validate_alumni__(alumni, extracted_data, fields)
            return alumni

        if response is not None:
            e = APIException(detail=mhs_list)
            e.status_code = response.status_code
            raise e
        raise APIException(detail='Something wrong')
