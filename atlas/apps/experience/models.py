from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _

from atlas.common.db.models import AbstractDateCreatedRecordable

User = get_user_model()


class Position(AbstractDateCreatedRecordable):
    """
    Represent work experience
    """
    owner = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='positions')

    title = models.CharField(_('Title'), max_length=64)
    company_name = models.CharField(_('Company'), max_length=64)
    description = models.TextField(_('Description'), max_length=64)
    location_name = models.CharField(_('Location'), max_length=64)
    industry_name = models.CharField(_('Industry'), max_length=64)

    date_started = models.DateField(_('Date Started'))
    date_ended = models.DateField(_('Date Ended'), null=True, blank=True)


class Education(AbstractDateCreatedRecordable):
    """
    Represent education experience
    """
    owner = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='educations')

    field_of_study = models.CharField(_('Field of Study'), max_length=64)
    school_name = models.CharField(_('School'), max_length=64)
    degree_name = models.CharField(_('Degree'), max_length=64)
    location_name = models.CharField(_('Location'), max_length=64)

    date_started = models.DateField(_('Date Started'))
    date_ended = models.DateField(_('Date Ended'), null=True, blank=True)
