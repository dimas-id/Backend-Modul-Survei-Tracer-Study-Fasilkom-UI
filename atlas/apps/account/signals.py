from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from atlas.apps.account.models import User, UserProfile
from atlas.apps.account.services import UserService
from atlas.clients.helios import UserHeliosManager
from atlas.clients.sendgrid import mail_manager
from atlas.libs import redis, client

user_service = UserService()


def send_registration_feedback(user):
    mail_manager.send_email(subject='Pendataan ILUNI12 Fasilkom UI',
                            to_emails=[user.email],
                            fail_silently=True,
                            html_content=f'<p>Hai {user.name}</p><br><p>Anda telah terdata di ILUNI12 Channel. ' + \
                                         'Saat ini Anda hanya dapat mengakses halaman Akun selama proses verifikasi. ' + \
                                         'Anda dapat melakukan pengecekan status verifikasi pada ' + \
                                         f'<a href="{settings.FRONTEND_URL}/users/">tautan ini</a>.</p>' + \
                                         '<p>Salam,</p><p>Tim ILUNI12</p>')


@receiver(post_save, sender=User, dispatch_uid='user_profile_creation')
def create_user_profile_on_new_user(sender, instance: User, created, **kwargs):
    """
    Create UserProfile for every new User
    """
    if created:
        UserProfile.objects.create(user=instance)

        # workaround, i think there is a bug related to args and kwargs
        redis.enqueue(send_registration_feedback, instance)


@receiver(post_save, sender=User, dispatch_uid='message_user_changes')
def message_about_user_changes(sender, instance: User, created, **kwargs):
    managers = [UserHeliosManager, ]
    for cls in managers:
        if issubclass(cls, client.UserManagerAdapter):
            redis.enqueue(cls().update_or_create_user, user_id=instance.id, user=instance)


@receiver(post_save, sender=UserProfile, dispatch_uid='verify_user_profile')
def verify_user_profile(sender, instance: UserProfile, created, **kwargs):
    if not created and not instance.user.is_verified:
        redis.enqueue(user_service.verify_user_registration, user=instance.user)
