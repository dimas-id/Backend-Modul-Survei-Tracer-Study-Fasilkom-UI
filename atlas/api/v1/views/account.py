from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenViewBase

from atlas.common.permissions import IsOwnerOfObject
from atlas.apps.account.serializers import \
    UserSerializer, RegisterUserSerializer, UserProfileSerializer, UserPreferenceSerializer,\
    UserTokenObtainPairSerializer
from atlas.apps.account.permissions import \
    IsAnonymous, AllowedRegister, HasPriviledgeToAccessUser
from atlas.apps.account.models import User, UserProfile, UserPreference


class UserTokenObtainPairView(TokenViewBase):
    serializer_class = UserTokenObtainPairSerializer


class UserCreateView(APIView):
    """
    post:
    Create user via registration. Must anonymous.
    """
    authentication_classes = ()
    permission_classes = (IsAnonymous, AllowedRegister)
    throttle_scope = 'register'

    def post(self, request, *args, **options):
        """
        user registration.
        create user and give back.
        """

        # validate data
        serializer = RegisterUserSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # save data
        user = serializer.save()
        return Response(data=UserSerializer(user).data, status=status.HTTP_201_CREATED, **options)


class UserDetailView(RetrieveUpdateAPIView):
    """
    get:
    retrieve the user and user profile

    put:
    Update full field of user and user profile

    patch:
    Update partial field of user and user profile
    """

    # we dont user IsOwnserOfObject because we need to check if user exists or not
    permission_classes = (IsAuthenticated, HasPriviledgeToAccessUser)
    serializer_class = UserSerializer
    lookup_field = 'pk'

    def get_object(self):
        """
        get user object.
        throw 404 if not found.
        """
        pk = self.kwargs.get(self.lookup_field)
        user = get_object_or_404(User, pk=pk)

        # check if user has permission to the user data
        self.check_object_permissions(self.request, user)
        return user


class UserPreferenceDetailView(RetrieveUpdateAPIView):
    """
    get:
    Retrieve user preference.

    put:
    Update user preference. Must be full field.

    patch:
    Update user preference. Partial field.
    """
    permission_classes = (IsOwnerOfObject,)
    serializer_class = UserPreferenceSerializer

    def get_object(self):
        """
        get user preference instance
        """
        preference = get_object_or_404(
            UserPreference, user=self.request.user)
        # we skip the self.check_object_permissions(preference)
        # because we get the preference from the user
        # not from lookup_field
        return preference
