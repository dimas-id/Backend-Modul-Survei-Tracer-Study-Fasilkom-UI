from django.utils import timezone
from atlas.apps.account.constants import C_PREFERENCES


def slugify_username(value):
    return value.replace(' ', '.')


def user_profile_pic_path(instance, filename):
    today = timezone.now()
    return f'users/{instance.user.id}/{today.year}/{today.month}/{today.day}/{filename}'


def default_preference():
    default = {}
    for p in C_PREFERENCES:
        default[p] = False
    return default
