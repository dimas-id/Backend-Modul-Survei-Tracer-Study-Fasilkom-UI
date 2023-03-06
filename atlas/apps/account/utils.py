from deprecated import deprecated
from django.utils import timezone

from atlas.apps.account.constants import C_PREFERENCES, C_TOP_SKILLS

import random
import string

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

def default_top_skills():
    default = {}
    for p in C_TOP_SKILLS:
        default[p] = False
    return default

def generate_random_password():
    all = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    temp = random.sample(all, random.randrange(8, 17))
    password = "".join(temp)
    
    return password
