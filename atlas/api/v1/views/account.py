from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from atlas.apps.account.serializers import (
    UserSerializer, RegisterUserSerializer, UserProfileSerializer)
from atlas.apps.account.permissions import (
    IsUserOwner, IsAnonymous, AllowedRegister, HasPriviledgeToMutateProfile
)
from atlas.apps.account.models import (User, UserProfile)


class UserCreateView(APIView):
    authentication_classes = ()
    permission_classes = (IsAnonymous, AllowedRegister)
    throttle_scope = 'register'

    def post(self, request, *args, **options):
        serializer = RegisterUserSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(data=UserSerializer(user).data, status=status.HTTP_201_CREATED, **options)


class UserDetailView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsUserOwner)
    serializer_class = UserSerializer

    def get_object(self):
        self.check_object_permissions(self.request, self.request.user)
        return self.request.user


class UserProfileDetailView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, HasPriviledgeToMutateProfile)
    serializer_class = UserProfileSerializer
    lookup_field = 'username'

    def get_object(self):
        """
        get user profile object,
        actually we can get profile with `self.request.user.profile` if only get own,
        but I just want state this explicitly and get other profile
        """
        username = self.kwargs.get('username')
        user_profile = get_object_or_404(UserProfile, user__username=username)
        self.check_object_permissions(self.request, user_profile)
        return user_profile
