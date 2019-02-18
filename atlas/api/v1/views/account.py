from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from atlas.apps.account.services import AuthService
from atlas.apps.account.serializers import AuthTokenSerializer
from atlas.apps.account.serializers import AccountSerializer
from atlas.apps.account.permissions import IsAccountOwner
from atlas.apps.account.models import Account


class LoginView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = 'login'

    auth_service = AuthService()

    def post(self, request):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            user = ser.validated_data['user']
            token = self.auth_service.generate_token(user)
            return Response({'token': token.key, 'account': AccountSerializer(instance=user).data})

        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    auth_service = AuthService()

    def post(self, request, *args, **kwargs):
        self.auth_service.clear_token(request.user)
        return Response({'message': 'OK'})


class AccountDetailView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsAccountOwner)
    serializer_class = AccountSerializer

    def get_object(self):
        return self.request.user


class TokenView(APIView):
    permission_classes = (IsAuthenticated,)
    auth_service = AuthService()

    def post(self, request, *args, **options):
        token = self.auth_service.get_token(request.user)
        return Response(
            data={'token': token.key},
            status=status.HTTP_200_OK)
