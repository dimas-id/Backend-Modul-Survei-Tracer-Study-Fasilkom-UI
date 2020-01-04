from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from atlas.apps.account.models import User
from atlas.apps.account.permissions import IsAnonymous
from atlas.apps.account.permissions import AllowedRegister
from atlas.apps.account.serializers import UserSerializer
from atlas.apps.account.serializers import RegisterUserSerializerV2

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
        serializer = RegisterUserSerializerV2(
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
