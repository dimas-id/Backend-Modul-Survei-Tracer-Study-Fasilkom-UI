from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from atlas.apps.account.models import User
from atlas.apps.account.permissions import VerifiedAccount
from atlas.apps.account.serializers import UserBatchRetrieveSerializer
from atlas.apps.account.serializers import UserSearchRetrieveSerializer

import functools
import operator
from django.db.models import Q

class UserSearchRetrieveView(ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSearchRetrieveSerializer
    permission_classes = [IsAuthenticated & (IsAdminUser|VerifiedAccount)]

    def get_queryset(self):
        queryset = User.objects.all()

        # all user
        name = self.request.query_params.get('name')
        csui_class_year = self.request.query_params.get('csui_class_year')
        csui_program = self.request.query_params.get('csui_program')
        company_name = self.request.query_params.get('company_name')
        title = self.request.query_params.get('title')
        industry_name = self.request.query_params.get('industry_name')

        # admin only
        gender = self.request.query_params.get('gender')
        residence_country = self.request.query_params.get('residence_country')
        start_csui_graduation_year = self.request.query_params.get('start_csui_graduation_year')
        start_csui_graduation_term = self.request.query_params.get('start_csui_graduation_term')
        end_csui_graduation_year = self.request.query_params.get('end_csui_graduation_year')
        end_csui_graduation_term = self.request.query_params.get('end_csui_graduation_term')
        
        # all user
        if name:
            queries = name.split()
            search_args = []
            for q in queries:
                for f in ('first_name__icontains', 'last_name__icontains'):
                    search_args.append(Q(**{f: q}))
            queryset = queryset.filter(functools.reduce(operator.or_, search_args))
        if csui_class_year:
            queryset = queryset.filter(educations__csui_class_year=csui_class_year)
        if csui_program:
            queryset = queryset.filter(educations__csui_program=csui_program)
        if company_name:
            queryset = queryset.filter(positions__company_name__icontains=company_name)
        if title:
            queryset = queryset.filter(positions__title__icontains=title)
        if industry_name:
            queryset = queryset.filter(positions__industry_name__icontains=industry_name)

        # admin only
        if self.request.user.is_staff:
            if gender:
                queryset = queryset.filter(profile__gender=gender)
            if residence_country:
                queryset = queryset.filter(profile__residence_country__icontains=residence_country)
            if start_csui_graduation_year and start_csui_graduation_term and end_csui_graduation_year and end_csui_graduation_term:
                search_args = []
                term = 0
                year = 0
                iteration = 0

                if int(start_csui_graduation_term) == 2: # lulus pada semester ganjil
                    if int(end_csui_graduation_term) == 1: #menangani penambahan tahun ketika lulus di semester genap
                        end_csui_graduation_year = int(end_csui_graduation_year) + 1

                    diff = int(end_csui_graduation_year) - int(start_csui_graduation_year)
                    if int(end_csui_graduation_term) == 2:
                        iteration = (diff * 2) + 1
                    else:
                        iteration = ((diff * 2) - 1) + 1

                    for i in range (iteration):
                        if i == 0:
                            term = int(start_csui_graduation_term)
                            year = int(start_csui_graduation_year)
                        elif i % 2 != 0:
                            term -= 1
                            year += 1
                        elif i % 2 == 0:
                            term += 1
                            year += 0
                        search_args.append(functools.reduce(operator.and_, [Q(**{'educations__csui_graduation_year': year}), Q(**{'educations__csui_graduation_term': term})]))
                else: # lulus pada semester genap
                    #menangani penambahan tahun ketika lulus di semester genap
                    start_csui_graduation_year = int(start_csui_graduation_year) + 1
                    if int(end_csui_graduation_term) == 1:
                        end_csui_graduation_year = int(end_csui_graduation_year) + 1
                    
                    diff = int(end_csui_graduation_year) - start_csui_graduation_year
                    if int(end_csui_graduation_term) == 1:
                        iteration = (diff * 2) + 1
                    else:
                        iteration = ((diff * 2) + 1) + 1

                    for i in range (iteration):
                        if i == 0:
                            term = int(start_csui_graduation_term)
                            year = int(start_csui_graduation_year)
                        elif i % 2 != 0:
                            term += 1
                            year += 0
                        elif i % 2 == 0:
                            term -= 1
                            year += 1
                        search_args.append(functools.reduce(operator.and_, [Q(**{'educations__csui_graduation_year': year}), Q(**{'educations__csui_graduation_term': term})]))
                
                query = search_args.pop()
                for item in search_args:
                    query |= item
                queryset = queryset.filter(query)
        
        return queryset
