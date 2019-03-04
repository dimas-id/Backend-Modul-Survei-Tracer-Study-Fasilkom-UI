from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from atlas.apps.account.serializers import (
    UserSerializer, RegisterUserSerializer, UserProfileSerializer)
from atlas.apps.account.permissions import (
    IsAnonymous, AllowedRegister, HasPriviledgeToAccessUser
)
from atlas.apps.account.models import (User, UserProfile)


class UserCreateView(APIView):
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
    permission_classes = (IsAuthenticated, HasPriviledgeToAccessUser)
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_object(self):
        """
        get user object.
        throw 404 if not found.
        """
        username = self.kwargs.get(self.lookup_field)
        user = get_object_or_404(User, username=username)

        # check if user has permission to the user data
        self.check_object_permissions(self.request, user)
        return user
