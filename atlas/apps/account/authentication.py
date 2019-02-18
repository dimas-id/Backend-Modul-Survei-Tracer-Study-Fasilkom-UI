from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

EXPIRE_HOURS = getattr(settings, 'AUTHENTICATION_TOKEN_EXPIRES_DURATION', 24)

class ExpiringTokenAuthentication(TokenAuthentication):

    model = Token # temporary fix: call self.model getting None

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted')

        if token.created < timezone.now() - timedelta(hours=EXPIRE_HOURS):
            raise AuthenticationFailed('Token has expired')

        return (token.user, token)