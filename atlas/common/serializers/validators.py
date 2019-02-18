from rest_framework.exceptions import ValidationError


def positive_integer_validator(value):
    if not isinstance(value, int) or value < 1:
        raise ValidationError('This field must be a positive integer')