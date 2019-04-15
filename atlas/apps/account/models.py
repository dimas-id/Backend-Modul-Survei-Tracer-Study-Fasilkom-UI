from django.db import models, transaction
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext as _
from django.conf import settings

from autoslug import AutoSlugField

from atlas.libs.db.models import (
    AbstractPrimaryUUIDable, AbstractTimestampable)
from atlas.apps.account.managers import UserManager
from atlas.apps.account.utils import (
    slugify_username,
    default_preference)
from atlas.libs.core.validators import PhoneRegex, NumericRegex


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
    ui_sso_npm = models.CharField(
        _("SSO UI NPM"), max_length=16, null=True, blank=True, validators=[NumericRegex()])

    #   linkedin
    #       @todo linkedin_id

    # preference
    # postgres implementation
    preference = JSONField(_('User Preference'),
                           default=default_preference,
                           help_text=_('Here is the user preference, we can add some later'))

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
    is_email_verified = models.BooleanField(
        _('Email Verified status'),
        default=False,
        help_text=_(
            'Designates that if this user email is not verified,'
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

    def set_as_verified(self):
        self.is_verified = True
        self.save(update_fields=('is_verified',))

    def __str__(self):
        return self.email


class UserProfile(AbstractTimestampable):
    """
    Represents User Profile, we store all personal related information here.
    """
    PROGRAM_CHOICES = (
        ('S1-IK', 'S1 - Ilmu Komputer'),
        ('S1_KI-IK', 'S1 KI - Ilmu Komputer'),
        ('S1-SI', 'S1 - Sistem Informasi'),
        ('S1_EKS-SI', 'S1 Ekstensi - Sistem Informasi'),
        ('S2-IK', 'S2 - Ilmu Komputer'),
        ('S2-TI', 'S2 - Teknologi Informasi'),
        ('S3-IK', 'S3 - Ilmu Komputer'),
    )
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))

    user = models.OneToOneField(
        primary_key=True, related_name='profile', to=User, on_delete=models.CASCADE)

    # personal info
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    phone_number = models.CharField(
        max_length=15, validators=[PhoneRegex()], null=True, blank=True)
    birthdate = models.DateField(null=True)

    # Residence
    residence_city = models.CharField(max_length=128, null=True, blank=True)
    residence_country = models.CharField(max_length=128, null=True, blank=True)
    residence_lng = models.FloatField(
        _('Residence Longitude'), null=True, blank=True)
    residence_lat = models.FloatField(
        _('Residence Latitude'), null=True, blank=True)

    # academic for validation purpose
    latest_csui_class_year = models.SmallIntegerField(
        _('Angkatan'), null=True, blank=True)
    latest_csui_program = models.CharField(
        _('Prodi'), choices=PROGRAM_CHOICES, max_length=10, blank=True)

    # most longest is Mengundurkan Diri/Keluar
    # provided by CSUI API
    # Kosong, Aktif, Cuti, Overseas, Mengundurkan diri/keluar
    latest_csui_graduation_status = models.CharField(
        _('Kelulusan'), max_length=32, blank=True, null=True)

    profile_pic_url = models.URLField(
        _('Profile Picture'), blank=True, default=settings.DEFAULT_PROFILE_PIC)

    website_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.name} ({self.latest_csui_class_year})'


def run_signal():
    import atlas.apps.account.signals


run_signal()
