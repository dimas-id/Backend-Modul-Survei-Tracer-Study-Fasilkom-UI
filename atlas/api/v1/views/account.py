from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from atlas.apps.account.serializers import (
    UserSerializer, RegisterUserSerializer)
from atlas.apps.account.permissions import (
    IsUserOwner, IsAnonymous, AllowedRegister
)
from atlas.apps.account.models import User


class UserCreateView(APIView):
    authentication_classes = ()
    permission_classes = (IsAnonymous, AllowedRegister)
    throttle_scope = 'register'

    def post(self, request, *args, **options):
        serializer = RegisterUserSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print(user)
        return Response(data=UserSerializer(user).data, status=status.HTTP_201_CREATED, **options)


class UserDetailView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsUserOwner)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
