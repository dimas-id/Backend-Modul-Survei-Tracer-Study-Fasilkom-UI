# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.generics import ListAPIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.permissions import IsAuthenticated, IsAdminUser

# from atlas.apps.account.models import User
# from atlas.apps.account.permissions import VerifiedAccount
# from atlas.apps.account.serializers import UserBatchRetrieveSerializer
# from atlas.apps.account.serializers import UserSearchRetrieveSerializer

# import functools
# import operator
# from django.db.models import Q

# class UserSearchRetrieveView(ListAPIView):

#     queryset = User.objects.all()
#     serializer_class = UserSearchRetrieveSerializer
#     permission_classes = [IsAuthenticated & (IsAdminUser|VerifiedAccount)]

#     def get_queryset(self):
#         queryset = User.objects.all()

#         name = self.request.query_params.get('name')
#         csui_class_year = self.request.query_params.get('csui_class_year')
#         csui_program = self.request.query_params.get('csui_program')
#         company_name = self.request.query_params.get('company_name')
#         title = self.request.query_params.get('title')
#         industry_name = self.request.query_params.get('industry_name')
#         gender = self.request.query_params.get('gender')
#         residence_country = self.request.query_params.get('residence_country')

#         """
#         kalo mau jadi satu path url, dia yg gender tetep bisa diisi ke query param, cuma ga ngefilter pencarian

#         """

#         if self.request.user.is_staff:
#             if gender:
#                 queryset = queryset.filter(profile__gender=gender)
#             if residence_country:
#                 queryset = queryset.filter(profile__residence_country__icontains=residence_country)

#         if name:
#             queries = name.split()
#             search_args = []
#             for q in queries:
#                 for f in ('first_name__icontains', 'last_name__icontains'):
#                     search_args.append(Q(**{f: q}))
#             queryset = queryset.filter(functools.reduce(operator.or_, search_args))
#         if csui_class_year:
#             queryset = queryset.filter(educations__csui_class_year=csui_class_year)
#         if csui_program:
#             queryset = queryset.filter(educations__csui_program=csui_program)
#         if company_name:
#             queryset = queryset.filter(positions__company_name__icontains=company_name)

#             """
#             buat multiple search, tapi kalo dia memenuhi kedua field, dia jadi muncul 2x di hasil search
#             jadi perlu difilter lagi munculnya sekali aja

#             company_name_list = self.request.GET.getlist('company_name')
#             search_args = []
#             for company in company_name_list:
#                 search_args.append(Q(**{'positions__company_name__icontains': company}))
#             queryset = queryset.filter(functools.reduce(operator.or_, search_args))
#             """
#         if title:
#             queryset = queryset.filter(positions__title__icontains=title)
#         if industry_name:
#             queryset = queryset.filter(positions__industry_name__icontains=industry_name)   
        
#         return queryset

# # class UserSearchRetrieveViewByUser(ListAPIView):

# #     queryset = User.objects.all()
# #     serializer_class = UserSearchRetrieveSerializerV1
# #     permission_classes = [IsAuthenticated & VerifiedAccount]

# #     def get_queryset(self):
# #         queryset = User.objects.all()

# #         name = self.request.query_params.get('name')
# #         csui_class_year = self.request.query_params.get('csui_class_year')
# #         csui_program = self.request.query_params.get('csui_program')
# #         company_name = self.request.query_params.get('company_name')
# #         title = self.request.query_params.get('title')
# #         industry_name = self.request.query_params.get('industry_name')

# #         if name:
# #             queries = name.split()
# #             search_args = []
# #             for q in queries:
# #                 for f in ('first_name__icontains', 'last_name__icontains'):
# #                     search_args.append(Q(**{f: q}))
# #             queryset = queryset.filter(functools.reduce(operator.or_, search_args))
# #         if csui_class_year:
# #             queryset = queryset.filter(educations__csui_class_year=csui_class_year)
# #         if csui_program:
# #             queryset = queryset.filter(educations__csui_program=csui_program)
# #         if company_name:
# #             queryset = queryset.filter(positions__company_name__icontains=company_name)
# #         if title:
# #             queryset = queryset.filter(positions__title__icontains=title)
# #         if industry_name:
# #             queryset = queryset.filter(positions__industry_name__icontains=industry_name)
        
# #         return queryset