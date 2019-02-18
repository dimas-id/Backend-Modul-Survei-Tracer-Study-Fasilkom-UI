from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.authentication import authenticate

from atlas.apps.account.models import Account


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_('Email'))
    password = serializers.CharField(
        label=_('Password'), style={'input_type': 'password'}, trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'), email=email.lower(), password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = {}
            if not email:
                msg['email'] = ['This field is required.']

            if not password:
                msg['password'] = ['This field is required.']

            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = (
            'name',
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'username',
            'last_login'
        )

        read_only_fields = (
            'name',
            'email',
            'username',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login'
        )
