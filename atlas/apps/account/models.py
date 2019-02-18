from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator

from autoslug import AutoSlugField

from atlas.common.db.models import AbstractPrimaryUUIDable
from atlas.common.db.models import AbstractDateCreatedRecordable
from atlas.apps.account.managers import UserManager
from atlas.apps.account.utils import slugify_username


class Account(AbstractBaseUser, PermissionsMixin, AbstractPrimaryUUIDable):
    """
    Represents account and authentication model
    """

    phone_regex = RegexValidator(
        regex=r'^\+?\d{9,15}$',
        message='Only digits are allowed. Country code are optional. ' 'Up to 15 digits allowed.',
    )

    # required fields
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    username = AutoSlugField(always_update=True,
                             sep="",
                             slugify=slugify_username,
                             populate_from='name',
                             unique=True,
                             editable=False)

    # additional informatin
    phone_number = models.CharField(
        max_length=15, validators=[phone_regex], null=True, blank=True)

    # some metas
    is_staff = models.BooleanField('Staff', default=False)
    is_superuser = models.BooleanField('Superuser', default=False)
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
