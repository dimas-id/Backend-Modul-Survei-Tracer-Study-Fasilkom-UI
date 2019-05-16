from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext as _


@deconstructible
class PhoneRegex(RegexValidator):

    regex = r'^\+?\d{9,15}$'
    message = _(
        'Only digits are allowed. Country code are optional. Up to 15 digits allowed.')
    code = 'invalid'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@deconstructible
class NumericRegex(RegexValidator):
    regex = r'^\d{9,11}$'
    message = _(
        'Only numeric are allowed. Up to 9-11 digits allowed.')
    code = 'invalid'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
