from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from atlas.apps.account.serializers import AuthTokenSerializer
from atlas.apps.account.serializers import AccountSerializer
from atlas.apps.account.permissions import IsAccountOwner
from atlas.apps.account.models import Account


class AccountDetailView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsAccountOwner)
    serializer_class = AccountSerializer

    def get_object(self):
        return self.request.user
