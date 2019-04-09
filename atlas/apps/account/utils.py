from django.utils import timezone
from deprecated import deprecated

from atlas.apps.account.constants import C_PREFERENCES


def slugify_username(value):
    return value.replace(' ', '.')


@deprecated(version='1.0', reason='Helios has endpoint for upload file. This function can\'t be deleted because a migration file needs this.')
def user_profile_pic_path(instance, filename):
    today = timezone.now()
    return f'users/{instance.user.id}/{today.year}/{today.month}/{today.day}/{filename}'


def default_preference():
    default = {}
    for p in C_PREFERENCES:
        default[p] = False
    return default


ui_npm_field = 'npm'
ui_name_field = 'name'
ui_birthdate_field = 'tgl_lahir'
ui_program_field = 'programs'
ui_class_year = 'angkatan'


def extract_alumni_data(mahasiswa_data):
    ui_name = mahasiswa_data.get(ui_name_field)
    ui_npm = mahasiswa_data.get(ui_npm_field)
    ui_birthdate = mahasiswa_data.get(ui_birthdate_field)
    ui_programs = mahasiswa_data.get(ui_program_field)
    ui_angkatan = -1
    ui_program = ''

    if ui_programs is not None and len(ui_programs) > 0:
        # take index 0 -> latest
        program = ui_programs[0]
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
        ui_angkatan = ui_program.get(ui_class_year)

    return (ui_name, ui_npm, ui_birthdate, ui_program, ui_angkatan)


def validate_alumni_data(user, ui_name, ui_npm, ui_birthdate, ui_program, ui_angkatan):
    """
    We are using scoring for validation and the minimum score is 65:
    npm: 15 points, because it is an optional field
    name: 25 points
        first_name 5 points, last_name: 10 points, full 10
    birthdate: 20 points
    csui_class: 20 points
    csui_program: 20 points
    """
    # get all field that we need
    npm = getattr(user, 'ui_sso_npm', None)
    csui_class = getattr(user.profile, 'latest_csui_class_year', None)
    birthdate = getattr(user.profile, 'birthdate', None)
    program = getattr(user.profile, 'latest_csui_program', None)

    validation_score = 0
    if ui_npm == npm:
        validation_score += 15

    if ui_birthdate == str(birthdate):
        validation_score += 20

    if ui_name.lower() == user.name.lower():
        validation_score += 25

    if ui_angkatan == csui_class:
        validation_score += 20

    if ui_program == program:
        validation_score += 20

    return validation_score >= 65
