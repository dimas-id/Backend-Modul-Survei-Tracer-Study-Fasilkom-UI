from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from django.contrib.postgres.fields import JSONField


class LinkedinAccount(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    email_address = models.EmailField(_('Linkedin User Email'), unique=True)
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)

    user_data = JSONField(_('Linkedin User Data'),
                          help_text=_('Here is the user linkedin data'))
