from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from atlas.apps.account.services import UserService
from atlas.libs import redis
from atlas.apps.account.models import User, UserProfile

@receiver(post_save, sender=User, dispatch_uid='user_profile_creation')
@transaction.atomic
def create_user_profile_on_new_user(sender, instance: User, created, **kwargs):
    """
    Create UserProfile for every new User
    """
    if created:
        UserProfile.objects.create(user=instance)

    if not instance.is_verified:
        redis.enqueue(UserService().verify_user_registration, user=instance)