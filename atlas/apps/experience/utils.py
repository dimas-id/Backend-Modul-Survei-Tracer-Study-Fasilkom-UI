
from atlas.apps.account.constants import (
    C_PREFERENCES,
    C_UI_NPM_FIELD,
    C_UI_NAME_FIELD,
    C_UI_BIRTHDATE_FIELD,
    C_UI_PROGRAMS_FIELD,
    C_UI_CLASS_YEAR_FIELD, )
from atlas.apps.experience.models import Education
from atlas.libs.string import get_most_matching, matching_partial

def extract_alumni_data(mahasiswa_data, input_program):
    ui_name = mahasiswa_data.get(C_UI_NAME_FIELD)
    ui_npm = mahasiswa_data.get(C_UI_NPM_FIELD)
    ui_birthdate = mahasiswa_data.get(C_UI_BIRTHDATE_FIELD)
    ui_programs = mahasiswa_data.get(C_UI_PROGRAMS_FIELD)
    ui_angkatan = -1
    ui_program = ''

    if ui_programs is not None and len(ui_programs) > 0:
        # take latest program and handle same NPM
        program = None
        for p in ui_programs:
            if p.get('nm_prg')[:2] == input_program:
                program = p
                break

        prg = program.get('nm_prg')
        degree = prg[:2]  # S1/S2/S3
        if 'Ekstensi' in prg:
            degree = degree + '_EKS'  # S1_EKS
        if 'International' in prg:
            degree = degree + '_KI'

        # get org
        # Ilmu Komputer -> [Ilmu, Komputer] -> [I, K] -> IK
        org = ''.join([s[:1] for s in program.get('nm_org').split()])

        ui_program = f'{degree}-{org}'.upper()
        # get ankgatan
        ui_angkatan = program.get(C_UI_CLASS_YEAR_FIELD)

    return (ui_name, ui_npm, ui_birthdate, ui_program, ui_angkatan)


def validate_alumni_data(education, ui_name, ui_npm, ui_birthdate, ui_program, ui_angkatan):
    """
    We are using scoring for validation and the minimum score is 70:
    npm: 15 points, because it is an optional field
    name: 25 points
        first_name 5 points, last_name: 10 points, full 10
    birthdate: 20 points
    csui_class: 20 points
    csui_program: 20 points
    """
    # get all field that we need
    npm = getattr(education, 'ui_sso_npm', None)
    csui_class = getattr(education, 'csui_class_year')
    birthdate = getattr(education.user.profile, 'birthdate')
    program = getattr(education, 'csui_program')

    validation_score = 0
    if str(ui_npm) == str(npm):
        validation_score += 15

    if str(ui_birthdate) == str(birthdate):
        validation_score += 20

    if str(ui_name).lower() == education.user.name.lower() or \
            matching_partial(str(ui_name).lower(), education.user.name.lower()) >= 75:
        validation_score += 25

    if ui_angkatan == csui_class:
        validation_score += 20

    if ui_program == program:
        validation_score += 20

    return validation_score >= 70


def get_most_matching_mahasiswa(mhs_list: list, target: str, extractor):
    """
    We matched one by one, and return mahasiswa with biggest ratio.
    """
    # create mapping
    # {'match1': index}
    mapping = {}
    # [match1, match2]
    matchs = []

    for i in range(len(mhs_list)):
        match = extractor(mhs_list[i])
        mapping[match] = i
        matchs.append(match)

    result = get_most_matching(target, matchs)

    if result:
        matched_string, ratio = result
        return mhs_list[mapping[matched_string]], ratio
    return (None, 0)


def check_verified_status(user):
    """
    Check user verification status.
    Rule: All education must be verified in order to verify the account
    """
    education_list = Education.objects.filter(user=user)
    is_verified = True
    for education in education_list:
        if not education.is_verified:
            is_verified = False
            break
    user.set_as_verified(is_verified)
