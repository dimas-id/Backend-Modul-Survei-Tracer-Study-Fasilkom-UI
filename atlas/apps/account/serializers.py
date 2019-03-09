from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.password_validation import (
    CommonPasswordValidator,
    MinimumLengthValidator,
    NumericPasswordValidator,
    UserAttributeSimilarityValidator,
)
from django.db import transaction

from rest_framework import serializers

from atlas.apps.account.services import AuthService
from atlas.apps.account.models import UserProfile, UserPreference
from atlas.apps.experience.serializers import PositionSerializer, EducationSerializer

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        exclude = ('user', 'latest_csui_graduation_status',)


class UserPreferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPreference
        exclude = ('user',)


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    positions = PositionSerializer(many=True)
    educations = EducationSerializer(many=True)

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Update User data and User Profile data
        """

        # updating profile data
        profile_data = validated_data.pop(User.PROFILE_FIELD)
        if profile_data:
            profile = instance.profile
            for profile_attr in profile_data.keys():
                # set attr profile with newest information from profile_data
                setattr(profile, profile_attr, profile_data[profile_attr])
            # little bit expensive to save all attribute
            # because not all attr in profile_data is valid
            # we cant set .save(update_fields=...)
            profile.save()

        # updating user data
        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'first_name',
            'last_name',
            'email',
            'username',
            'profile',
            'positions',
            'educations',
            'groups',
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
            'positions',
            'educations',
            'groups',
            'last_login',
            'is_active',
            'is_staff',
            'is_superuser',
            'is_verified',
        )


class RegisterUserSerializer(serializers.Serializer):
    username_field = User.USERNAME_FIELD
    MIN_GENERATION = 1986

    # auth
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    # profile
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    birthdate = serializers.DateField()

    # academic data
    ui_sso_npm = serializers.CharField(max_length=16, required=False)
    latest_csui_class = serializers.IntegerField(
        min_value=MIN_GENERATION, max_value=timezone.now().year)
    latest_csui_program = serializers.CharField()

    def create(self, validated_data):
        """
        create user based on validated data
        """
        auth_service = AuthService()
        request = self.context.get('request')
        return auth_service.registerPublicUser(
            request, identifier=validated_data[self.username_field], **validated_data)

    def validate(self, attrs):
        """
        Validate data that anonymous send in registration.
        Raise serializers.ValidationException if data is not valid.
        """
        identifier = attrs.get(self.username_field)
        password = attrs.get('password')
        request = self.context.get('request')

        error = {}

        # normalize email
        if self.username_field == 'email':
            attrs[self.username_field] = identifier = identifier.lower()
            if identifier.endswith('@ui.ac.id'):
                error[self.username_field] = [
                    'Can\'t register using UI email.']

        # validate password to minimum
        MinimumLengthValidator(min_length=8).validate(password)
        CommonPasswordValidator().validate(password)
        UserAttributeSimilarityValidator(password, request.user)
        NumericPasswordValidator().validate(password)

        # validate identifier (email/username) is unique
        if User.objects.filter(**{self.username_field: identifier}).exists():
            error[self.username_field] = [
                f'{self.username_field} is already exists']

        if len(error) > 0:
            raise serializers.ValidationError(
                error, code='invalid_registration')

        return attrs
