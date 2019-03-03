from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext as _

from autoslug import AutoSlugField

from atlas.common.db.models import (
    AbstractPrimaryUUIDable, AbstractTimestampable)
from atlas.apps.account.managers import UserManager
from atlas.apps.account.utils import slugify_username
from atlas.common.core.validators import PhoneRegex


class User(AbstractBaseUser, PermissionsMixin, AbstractPrimaryUUIDable, AbstractTimestampable):
    """
    Represents User and authentication model.
    """
    # required fields
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    username = AutoSlugField(always_update=True,
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
    is_superuser = models.BooleanField(_('Superuser'), default=False)
    is_staff = models.BooleanField(_('Staff'), default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
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
    def is_verified(self):
        """
        @todo implement this later,
        """
        return False

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
        ("TL", "Tidak Lulus"),
        ("BL", "Belum Lulus"),
        ("SL", "Sudah Lulus"),
    )
    GENDER_CHOICES = (("M", "Male"), ("F", "Female"))

    user = models.OneToOneField(
        related_name='profile', to=User, on_delete=models.CASCADE)

    # personal info
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    phone_number = models.CharField(
        max_length=15, validators=[PhoneRegex()], null=True, blank=True)
    birthplace = models.CharField(max_length=128)
    birthdate = models.DateField(null=True)

    # Residence
    residence_city = models.CharField(max_length=128, null=True, blank=True)
    residence_country = models.CharField(max_length=128, null=True, blank=True)

    # angkatan
    # if user has bachelor degree from Fasilkom UI, then use the
    # angkatan when user was still undergraduate.
    # else if user doesnt
    latest_csui_generation = models.SmallIntegerField(
        _('Angkatan'), null=True, blank=True)
    latest_csui_graduation_status = models.CharField(
        _("Kelulusan"), choices=GRADUATION_CHOICES, max_length=1, null=True, blank=True)

    # others
    profile_pic_url = models.URLField(
        _('Profile Picture'), null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.name} ({self.latest_csui_generation})'


@receiver(post_save, sender=User, dispatch_uid='user_profile_creation')
@transaction.atomic
def create_user_profile_on_new_user(sender, instance: User, created, **kwargs):
    """
    Create UserProfile for every new User
    """
    if created:
        UserProfile.objects.create(user=instance)
