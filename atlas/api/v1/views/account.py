from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase

from atlas.api.v1.views.experience import experience_service
from atlas.apps.account.models import User
from atlas.apps.account.permissions import \
    IsAnonymous, AllowedRegister, HasPriviledgeToAccessUser
from atlas.apps.account.serializers import \
    UserSerializer, RegisterUserSerializer, UserPreferenceSerializer, \
    UserTokenObtainPairSerializer
from atlas.apps.experience.models import Education
from atlas.libs import redis
from atlas.libs.permissions import IsOwnerOfObject


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

        # manually create jwt token
        refresh_token = RefreshToken.for_user(user)

        return Response(
            data={
                'refresh': str(refresh_token),
                'access': str(refresh_token.access_token),
                'user': UserSerializer(user).data},
            status=status.HTTP_201_CREATED, **options)


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
    permission_classes = [IsAuthenticated & (HasPriviledgeToAccessUser|IsAdminUser)]
    serializer_class = UserSerializer
    lookup_field = 'pk'

    def get_object(self):
        """
        get user object.
        throw 404 if not found.
        """
        pk = self.kwargs.get(self.lookup_field)
        try:
            user = get_object_or_404(User, pk=pk, is_active=True)
        except ValidationError:
            # fix uuid validation error pk='random string'
            raise Http404

        # check if user has permission to the user data
        self.check_object_permissions(self.request, user)
        return user

    def patch(self, request, *args, **kwargs):
        patch = self.partial_update(request, *args, **kwargs)
        educations = Education.objects.filter(user=kwargs.get(self.lookup_field)  if IsAdminUser else request.user)
        for education in educations:
            redis.enqueue(experience_service.verify_user_registration, education=education)
        return patch


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
        return self.request.user
