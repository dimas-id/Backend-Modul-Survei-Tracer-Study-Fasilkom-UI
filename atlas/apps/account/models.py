from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext as _

from autoslug import AutoSlugField

from atlas.common.db.models import AbstractPrimaryUUIDable
from atlas.common.db.models import AbstractDateCreatedRecordable
from atlas.apps.account.managers import UserManager
from atlas.apps.account.utils import slugify_username
from atlas.common.core.validators import PhoneRegex

class User(AbstractBaseUser, PermissionsMixin, AbstractPrimaryUUIDable):
    """
    Represents User and authentication model
    """
    # required fields
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    username = AutoSlugField(always_update=True,
                             sep="",
                             slugify=slugify_username,
                             populate_from='name',
                             unique=True,
                             editable=False)
    phone_number = models.CharField(
            max_length=15, validators=[PhoneRegex()], null=True, blank=True)

    profile_pic_url = models.URLField(_('Profile Picture'), null=True, blank=True)

    # external authentications
    #   CAS SSO UI
    ui_sso_username = models.CharField(
        _("SSO UI username"), max_length=64, blank=True, null=True, unique=True
    )
    #       UI lecturers and staff might not have this field, but it's nice to have
    #       this field for later analysis
    # ui_sso_npm = models.CharField(
    #     _("SSO UI NPM"), max_length=16, blank=True, null=True)

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
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.name} <{self.email}>'
