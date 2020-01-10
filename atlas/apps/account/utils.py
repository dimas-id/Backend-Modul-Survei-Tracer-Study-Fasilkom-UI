from deprecated import deprecated
from django.utils import timezone

from atlas.apps.account.constants import (
    C_PREFERENCES,
    C_UI_NPM_FIELD,
    C_UI_NAME_FIELD,
    C_UI_BIRTHDATE_FIELD,
    C_UI_PROGRAMS_FIELD,
    C_UI_CLASS_YEAR_FIELD, )
from atlas.libs.string import get_most_matching, matching_partial


def slugify_username(value):
    return value.replace(' ', '.')


@deprecated(version='1.0',
            reason='Helios has endpoint for upload file. This function can\'t be deleted because a migration file needs this.')
def user_profile_pic_path(instance, filename):
    today = timezone.now()
    return f'users/{instance.user.id}/{today.year}/{today.month}/{today.day}/{filename}'


def default_preference():
    default = {}
    for p in C_PREFERENCES:
        default[p] = False
    return default

