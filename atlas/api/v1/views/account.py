from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from atlas.apps.account.serializers import UserSerializer
from atlas.apps.account.permissions import IsUserOwner
from atlas.apps.account.models import User


class UserDetailView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsUserOwner)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
