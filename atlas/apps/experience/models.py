from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext as _

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
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='educations')

    field_of_study = models.CharField(_('Field of Study'), max_length=64)
    school_name = models.CharField(_('School'), max_length=64)
    degree_name = models.CharField(_('Degree'), max_length=64)
    location_name = models.CharField(_('Location'), max_length=64)

    date_started = models.DateField(_('Date Started'))
    date_ended = models.DateField(_('Date Ended'))
