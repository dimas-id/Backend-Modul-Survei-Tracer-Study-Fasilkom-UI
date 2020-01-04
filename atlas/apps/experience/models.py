from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext as _

from atlas.libs.core.validators import NumericRegex
from atlas.libs.db.models import AbstractDateCreatedRecordable

User = get_user_model()


class Position(AbstractDateCreatedRecordable):
    """
    Represent work experience
    """
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='positions')

    title = models.CharField(_('Title'), max_length=64)
    company_name = models.CharField(_('Company'), max_length=64)
    location_name = models.CharField(_('Location'), max_length=64, null=True)
    industry_name = models.CharField(_('Industry'), max_length=64)

    date_started = models.DateField(_('Date Started'))
    date_ended = models.DateField(_('Date Ended'), null=True, blank=True)

    company_metadata = JSONField(null=True, blank=True, help_text=_(
        'Here is company metadata comes from linkedin'))

    @property
    def is_current(self):
        return self.date_ended is None


class Education(AbstractDateCreatedRecordable):
    """
    Represent education experience
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

    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='educations')

    ui_sso_npm = models.CharField(
        _("SSO UI NPM"), max_length=16, null=True, blank=True, validators=[NumericRegex()], db_index=True)

    # academic for validation purpose
    csui_class_year = models.SmallIntegerField(
        _('Angkatan'), null=True, blank=True)
    csui_program = models.CharField(
        _('Prodi'), choices=PROGRAM_CHOICES, max_length=10, blank=True)

    # most longest is Mengundurkan Diri/Keluar
    # provided by CSUI API
    # Kosong, Aktif, Cuti, Overseas, Mengundurkan diri/keluar
    csui_graduation_status = models.CharField(
        _('Kelulusan'), max_length=32, blank=True, null=True)
