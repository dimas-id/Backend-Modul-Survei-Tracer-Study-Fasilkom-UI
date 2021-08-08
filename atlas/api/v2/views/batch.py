from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from atlas.apps.account.models import User
from atlas.apps.account.permissions import IsAnonymous
from atlas.apps.account.permissions import AllowedRegister
from atlas.apps.account.serializers import UserBatchRetrieveSerializer
from atlas.apps.account.serializers import RegisterUserSerializerV2

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class UserBatchRetrieveView(ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserBatchRetrieveSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated & IsAdminUser]

    def get_queryset(self):
        queryset = User.objects.all()
        program = self.request.query_params.get('program')
        year = self.request.query_params.get('year')
        operator = self.request.query_params.get('operator','eq')
        if program:
            queryset = queryset.filter(educations__csui_program=program)
        if year:
            if operator == 'eq':
                queryset = queryset.filter(educations__csui_class_year=year)
            elif operator == 'gte':
                queryset = queryset.filter(educations__csui_class_year__gte=year)
            elif operator == 'lte':
                queryset = queryset.filter(educations__csui_class_year__lte=year)
        return queryset