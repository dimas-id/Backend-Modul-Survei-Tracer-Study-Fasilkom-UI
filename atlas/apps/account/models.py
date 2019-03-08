from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext as _
from django.conf import settings

from autoslug import AutoSlugField

from atlas.common.db.models import (
    AbstractPrimaryUUIDable, AbstractTimestampable)
from atlas.apps.account.managers import UserManager
from atlas.apps.account.utils import slugify_username, user_profile_pic_path
from atlas.common.core.validators import PhoneRegex


class User(AbstractBaseUser, PermissionsMixin, AbstractPrimaryUUIDable, AbstractTimestampable):
    """
    Represents User and authentication model.
    """
    # required fields
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)

    # public ID
    # default DB index is True
    username = AutoSlugField(always_update=False,
                             sep="",
                             slugify=slugify_username,
                             populate_from='name',
                             unique=True,
                             editable=False)

    # external authentications

    # CAS SSO UI
    ui_sso_username = models.CharField(
        _("SSO UI username"), max_length=64, null=True, blank=True, unique=True
    )
    # UI lecturers and staff might not have this field, but it's nice to have
    # this field for later analysis
    ui_sso_npm = models.CharField(
        _("SSO UI NPM"), max_length=16, null=True, blank=True)

    #   linkedin
    #       @todo linkedin_id

    # some metas
    is_superuser = models.BooleanField(
        _('Superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ))
    is_staff = models.BooleanField(
        _('Staff status'),
        default=False,
        help_text=_(
            'Designates that this user can login to administrator site.'
        ))
    is_active = models.BooleanField(
        _('Active status'),
        default=True,
        help_text=_(
            'Designates that if this user is not active, then can\'t login.'
        ))
    is_verified = models.BooleanField(
        _('Verified status'),
        default=False,
        help_text=_(
            'Designates that if this user is not verified,'
            'then can\'t access other services except Account Service'
        ))

    USERNAME_FIELD = 'email'
    PROFILE_FIELD = 'profile'
    REQUIRED_FIELDS = (
        'first_name',
        'last_name'
    )

    objects = UserManager()

    @property
    def name(self):
        """
        returns full name
        """
        return f'{self.first_name} {self.last_name}'

    @property
    def is_paired_sso(self):
        """
        returns true if user has paired this account with SSO UI
        """
        return self.ui_sso_username is not None

    def __str__(self):
        return self.email


class UserProfile(AbstractTimestampable):
    """
    Represents User Profile, we store all personal related information here.
    """
    GRADUATION_CHOICES = (
        ('TL', 'Tidak Lulus'),
        ('BL', 'Belum Lulus'),
        ('SL', 'Sudah Lulus'),
    )
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))

    user = models.OneToOneField(
        primary_key=True, related_name='profile', to=User, on_delete=models.CASCADE)

    # personal info
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    phone_number = models.CharField(
        max_length=15, validators=[PhoneRegex()], null=True, blank=True)

    # todo: remove birthplace
    birthplace = models.CharField(max_length=128)
    birthdate = models.DateField(null=True)

    # Residence
    residence_city = models.CharField(max_length=128, null=True, blank=True)
    residence_country = models.CharField(max_length=128, null=True, blank=True)

    # academic for validation purpose
    latest_csui_generation = models.SmallIntegerField(
        _('Angkatan'), null=True, blank=True)
    latest_csui_program = models.CharField(
        _('Prodi'), max_length=64, blank=True)
    latest_csui_graduation_status = models.CharField(
        _('Kelulusan'), choices=GRADUATION_CHOICES, max_length=2, blank=True)

    # upload profile pic to AWS to MEDIA_ROOT/users/<user_id>/<year>/<filename>
    # default is upload default profile pic
    profile_pic_url = models.ImageField(
        _('Profile Picture'), blank=True, upload_to=user_profile_pic_path, default=settings.DEFAULT_PROFILE_PIC)

    website_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.name} ({self.latest_csui_generation})'


class UserPreference(AbstractTimestampable):
    """
    Represent user preference, add other preference later if we need.
    """
    user = models.OneToOneField(
        related_name='preference', to=User, on_delete=models.CASCADE)

    # preferences
    should_send_newsletter = models.BooleanField(
        _('Send Newsletter'),
        default=True,
        help_text=_(
            'Designates that if this is active, '
            'then user should receive email about Newsletter.'
        ))
    should_send_event = models.BooleanField(
        _('Send Event Update'),
        default=True,
        help_text=_(
            'Designates that if this is active, '
            'then user should receive email about Event update.'
        ))
    should_send_vacancy = models.BooleanField(
        _('Send Vacancy Update'),
        default=True,
        help_text=_(
            'Designates that if this is active, '
            'then user should receive email about Vacancy update.'
        ))
    should_send_donation_info = models.BooleanField(
        _('Send Donation Information'),
        default=True,
        help_text=_(
            'Designates that if this is active, '
            'then user should receive email about Donation information.'
        ))
    should_send_update = models.BooleanField(
        _('Send General Update'),
        default=True,
        help_text=_(
            'Designates that if this is active, '
            'then user should receive email about General update.'
        ))
    could_contact_me = models.BooleanField(
        _('Contact the person, personally'),
        default=False,
        help_text=_(
            'Designates that if this is active, '
            'then we could contact user as Fasilkom UI about matter.'
        ))

    def __str__(self):
        return self.user.name


@receiver(post_save, sender=User, dispatch_uid='user_profile_creation')
@transaction.atomic
def create_user_profile_on_new_user(sender, instance: User, created, **kwargs):
    """
    Create UserProfile and UserPreference for every new User
    """
    if created:
        UserProfile.objects.create(user=instance)
        UserPreference.objects.create(user=instance)
