from atlas.apps.validator.constants import (
    C_UI_NPM_FIELD,
    C_UI_NAME_FIELD,
    C_UI_BIRTHDATE_FIELD,
    C_UI_PROGRAMS_FIELD,
    C_UI_CLASS_YEAR_FIELD,
    C_UI_ADDRESS,
    C_UI_CITY_BIRTH,
    C_UI_ORG,
    C_UI_STATUS
)
from atlas.libs.string import get_most_matching, matching_partial
from atlas.apps.validator.models import AlumniValidation


def extract_alumni_data(mahasiswa_data: dict):
    ui_name = mahasiswa_data.get(C_UI_NAME_FIELD)
    ui_npm = mahasiswa_data.get(C_UI_NPM_FIELD)
    ui_birthdate = mahasiswa_data.get(C_UI_BIRTHDATE_FIELD)
    ui_programs = mahasiswa_data.get(C_UI_PROGRAMS_FIELD)
    ui_address = mahasiswa_data.get(C_UI_ADDRESS)
    ui_city_birth = mahasiswa_data.get(C_UI_CITY_BIRTH)
    ui_angkatan = -1
    ui_program = ''
    ui_status = ''

    if ui_programs is not None and len(ui_programs) > 0:
        # take index 0 -> latest
        program = ui_programs[0]
        ui_program = program.get(C_UI_ORG)
        # get ankgatan
        ui_angkatan = program.get(C_UI_CLASS_YEAR_FIELD)
        ui_status = program.get(C_UI_STATUS)

    return {C_UI_NAME_FIELD: ui_name,
            C_UI_NPM_FIELD: ui_npm,
            C_UI_BIRTHDATE_FIELD: ui_birthdate,
            C_UI_ORG: ui_program,
            C_UI_ADDRESS: ui_address,
            C_UI_CITY_BIRTH: ui_city_birth,
            C_UI_CLASS_YEAR_FIELD: ui_angkatan,
            C_UI_STATUS: ui_status}


def validate_name(alumni_name, mhs_name):
    nama = str(alumni_name).lower()
    nama_valid = mhs_name.lower()

    if nama in nama_valid and \
            matching_partial(nama, nama_valid) >= 85:
        return True
    return False


def validate_npm(alumni_npm, mhs_npm):
    return alumni_npm == mhs_npm


def validate_birthdate(alumni_birthdate, mhs_birthdate):
    return alumni_birthdate == mhs_birthdate


def validate_angkatan(alumni_angkatan, mhs_angkatan):
    return alumni_angkatan == mhs_angkatan


def validate_org(alumni_org, mhs_org):
    return str(alumni_org).lower() == mhs_org.lower()


def validate_alumni_data(alumni: AlumniValidation, mhs_data: dict, fields: set = None):
    validation_score = 0

    if fields and len(fields) > 0:
        max_score = len(fields)
        for fd in fields:
            if fd == C_UI_NPM_FIELD:
                validation_score += validate_npm(
                    alumni.npm, mhs_data.get(C_UI_NPM_FIELD))

            elif fd == C_UI_BIRTHDATE_FIELD:
                validation_score += validate_birthdate(
                    alumni.tgl_lahir, mhs_data.get(C_UI_BIRTHDATE_FIELD))

            elif fd == C_UI_NAME_FIELD:
                validation_score += validate_name(
                    alumni.nama, mhs_data.get(C_UI_NAME_FIELD))

            elif fd == C_UI_CLASS_YEAR_FIELD:
                validation_score += validate_angkatan(
                    alumni.angkatan, mhs_data.get(C_UI_CLASS_YEAR_FIELD))

            elif fd == C_UI_ORG:
                validation_score += validate_angkatan(
                    alumni.nm_org, mhs_data.get(C_UI_ORG))
    else:
        max_score = 3

        # one of them (npm or name) must be satisfied
        if alumni.npm is not None:
            max_score += 1
            validation_score += validate_npm(
                alumni.npm, mhs_data.get(C_UI_NPM_FIELD))

        if alumni.nama is not None:
            max_score += 1
            validation_score += validate_name(
                alumni.nama, mhs_data.get(C_UI_NAME_FIELD))

        validation_score += validate_birthdate(
            alumni.tgl_lahir, mhs_data.get(C_UI_BIRTHDATE_FIELD))
        validation_score += validate_angkatan(
            alumni.angkatan, mhs_data.get(C_UI_CLASS_YEAR_FIELD))
        validation_score += validate_org(
            alumni.nm_org, mhs_data.get(C_UI_ORG))

    return validation_score // max_score >= 1


def get_most_matching_mahasiswa(mhs_list: list, target: str, extractor):
    """
    We matched one by one, and return mahasiswa with biggest ratio.
    """
    # create mapping
    # {'match1': index}
    mapping = {}
    # [match1, match2]
    matches = []

    for i in range(len(mhs_list)):
        match = extractor(mhs_list[i])
        mapping[match] = i
        matches.append(match)

    result = get_most_matching(target, matches)

    if result:
        matched_string, ratio = result
        return mhs_list[mapping[matched_string]], ratio
    return None, 0
