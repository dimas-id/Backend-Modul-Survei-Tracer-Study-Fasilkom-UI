from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.password_validation import (
    CommonPasswordValidator,
    MinimumLengthValidator,
    NumericPasswordValidator,
    UserAttributeSimilarityValidator,
)

from rest_framework import serializers

from atlas.apps.account.services import AuthService
from atlas.apps.account.models import UserProfile

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        exclude = ('user',)


class UserSerializer(serializers.ModelSerializer):

    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = (
            'name',
            'first_name',
            'last_name',
            'email',
            'username',
            'profile',
            'last_login',
            'is_verified',
            'is_active',
            'is_staff',
            'is_superuser',
            'is_verified',
        )

        read_only_fields = (
            'name',
            'email',
            'username',
            'last_login',
            'is_active',
            'is_staff',
            'is_superuser',
            'is_verified',
        )


class RegisterUserSerializer(serializers.Serializer):
    username_field = User.USERNAME_FIELD

    # auth
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    # profile
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    birthplace = serializers.CharField()
    birthdate = serializers.DateField()

    # academic data
    ui_sso_npm = serializers.CharField(max_length=16, required=False)
    latest_csui_generation = serializers.IntegerField()

    def create(self, validated_data):
        auth_service = AuthService()
        request = self.context.get('request')
        return auth_service.registerPublicUser(
            request, identifier=validated_data[self.username_field], **validated_data)

    def validate(self, attrs):
        identifier = attrs.get(self.username_field)
        password = attrs.get('password')
        request = self.context.get('request')

        error = {}
        if self.username_field == 'email':
            attrs[self.username_field] = identifier = identifier.lower()
            if identifier.endswith('@ui.ac.id'):
                error[self.username_field] = [
                    'Can\'t register using UI email.']

        MinimumLengthValidator(min_length=8).validate(password)
        CommonPasswordValidator().validate(password)
        UserAttributeSimilarityValidator(password, request.user)
        NumericPasswordValidator().validate(password)

        if attrs['latest_csui_generation'] < 0 or attrs['latest_csui_generation'] > timezone.now().year:
            error['latest_csui_generation'] = [
                'There is no such generation yet']

        if len(error) > 0:
            raise serializers.ValidationError(
                error, code='invalid_registration')

        return attrs
