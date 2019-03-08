from django.utils import timezone

def slugify_username(value):
    return value.replace(' ', '.')

def user_profile_pic_path(instance, filename):
    today = timezone.now()
    return f'users/{instance.user.id}/{today.year}/{today.month}/{today.day}/{filename}'