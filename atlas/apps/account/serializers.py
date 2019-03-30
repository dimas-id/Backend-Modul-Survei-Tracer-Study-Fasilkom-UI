from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.password_validation import (
    CommonPasswordValidator,
    MinimumLengthValidator,
    NumericPasswordValidator,
    UserAttributeSimilarityValidator)
from django.db import transaction

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from atlas.apps.account.services import UserService
from atlas.apps.account.models import UserProfile
from atlas.apps.experience.serializers import PositionSerializer, EducationSerializer
from atlas.apps.account.constants import C_PREFERENCES

User = get_user_model()


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        exclude = ('user', 'latest_csui_graduation_status',)

    def validate_residence_lng(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError(
                detail='Invalid Residence Longitude', code='invalid_profile')
        return value

    def validate_residence_lat(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError(
                detail='Invalid Residence Latitude', code='invalid_profile')
        return value


class UserPreferenceSerializer(serializers.ModelSerializer):

    preference = serializers.JSONField()

    def validate_preference(self, new_preference: dict):
        if type(new_preference) is not dict:
            # JSON object only
            raise serializers.ValidationError(
                detail='Invalid object', code='invalid_preference')

        validated_preference = {}
        # just get the value that in C_PREFERENCES
        for c in C_PREFERENCES:
            selected_preference = new_preference.get(c, None)
            if selected_preference is not None:
                validated_preference[c] = selected_preference

        return validated_preference

    def update(self, instance, validated_data):
        PREFERENCE = 'preference'

        # update preference
        preference = dict(getattr(instance, PREFERENCE))
        preference.update(validated_data.get(PREFERENCE))

        # immutable
        new_validated_data = dict(validated_data)
        new_validated_data[PREFERENCE] = preference

        return super().update(instance, new_validated_data)

    class Meta:
        model = User
        read_only_fields = ('id',)
        fields = ('id', 'preference')


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    groups = serializers.SerializerMethodField()

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

    def get_groups(self, instance):
        groups = instance.groups
        group_names = [g.name for g in groups.all()]
        return group_names

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
    latest_csui_class_year = serializers.IntegerField(
        min_value=MIN_GENERATION, max_value=timezone.now().year)
    latest_csui_program = serializers.CharField()

    def create(self, validated_data):
        """
        create user based on validated data
        """
        auth_service = UserService()
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
