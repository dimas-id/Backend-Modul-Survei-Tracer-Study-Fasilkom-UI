import pytz
from datetime import datetime

from django.utils import timezone
from django.db import transaction
from django.conf import settings

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication


class AuthService:

    @transaction.atomic
    def generate_token(self, user):
        '''
        Generate token if doesn't exist.
        '''
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            # update the created time of the token to keep it valid
            token.created = datetime.utcnow().replace(tzinfo=pytz.utc)
            token.save(update_fields=('created',))

        return token

    def clear_token(self, user):
        tokens = Token.objects.filter(user=user)
        if tokens.exists():
            tokens.delete()

    def get_token(self, user):
        return Token.objects.get(user=user)
