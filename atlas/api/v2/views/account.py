from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken
import requests

from atlas.apps.account.models import User
from atlas.apps.account.permissions import IsAnonymous
from atlas.apps.account.permissions import AllowedRegister
from atlas.apps.account.serializers import UserSerializer, UserFullDetailByAdminSerializer
from atlas.apps.account.serializers import RegisterUserSerializerV2, RegisterBulkUserSerializerV2
from atlas.apps.experience.serializers import EducationSerializer, PositionSerializer
from atlas.apps.experience.models import Position, Education, OtherEducation
from atlas.libs import redis
from atlas.apps.experience.services import ExperienceService
from django.conf import settings
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import re, json, csv

from django.http import HttpResponse
import functools
import operator
from django.db.models import Q

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

        print(serializer)

        # save data
        user = serializer.save()
        print("berhasil")

        # manually create jwt token
        refresh_token = RefreshToken.for_user(user)

        return Response(
            data={
                'refresh': str(refresh_token),
                'access': str(refresh_token.access_token),
                'user': UserSerializer(user).data},
            status=status.HTTP_201_CREATED, **options)

class BulkUserCreateView(APIView):
    """
    post:
    Create bulk user via registration. Must admin.
    """
    permission_classes = [IsAuthenticated & IsAdminUser]
    throttle_scope = 'register'

    def post(self, request, *args, **options):
        """
        user registration.
        create user and give back.
        """

        list_user_success = []
        list_user_failed = []

        # print(settings.SISIDANG_RESPONSE)
        respon = settings.SISIDANG_RESPONSE

        # for alumni in request.data:
        for alumni in respon:

            try:
                education_data = alumni.get('education')
                position_data = alumni.get('position')
            except KeyError:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # validate data
                serializer = RegisterBulkUserSerializerV2(
                    data=alumni, context={'request': request})
                serializer.is_valid(raise_exception=True)

                serializer_edu = EducationSerializer(data=education_data)
                serializer_edu.is_valid(raise_exception=True)

                if(position_data.get('title') != '' and position_data.get('company_name') != '' and position_data.get('industry_name') != '' and position_data.get('location_name') != '' and position_data.get('date_started') != ''):
                    serializer_pos = PositionSerializer(data=position_data)
                    serializer_pos.is_valid(raise_exception=True)
                
                # save data
                user = serializer.save()

                # verifikasi education
                Education.objects.filter(user=user).delete()
                education = serializer_edu.save(user=user)

                experience_service = ExperienceService()
                # redis.enqueue(experience_service.verify_user_registration, education=education)
                experience_service.verify_user_registration(education=education)

                if(position_data.get('title') != '' and position_data.get('company_name') != '' and position_data.get('industry_name') != '' and position_data.get('location_name') != '' and position_data.get('date_started') != ''):
                    position = serializer_pos.save(user=user)

                list_user_success.append(UserFullDetailByAdminSerializer(user).data)
            
            except Exception as e:
                exp_msg = (str(e))
                print(exp_msg)
                error_reason = re.findall(r"'([^\",()=\[\]]*?):",exp_msg)
                
                for i in range(len(error_reason)):
                    error_reason[i] = error_reason[i].split('\'')[0]

                user = []
                user.append(alumni)
                user.append(error_reason)
                list_user_failed.append(user)
                continue

        return Response(
            data={
                'user_success': list_user_success,
                'user_failed': list_user_failed},
            status=status.HTTP_201_CREATED, **options)

class ExportCSVStudents(ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserFullDetailByAdminSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    
    def get(self, request, format=None):
        """
        Filtering
        """
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

        """
        Exporting
        """
        ser = UserFullDetailByAdminSerializer(queryset, many=True)
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'

        writer = csv.DictWriter(response, fieldnames = ["name", "email", "gender", "phone", "birth_date", "city", "country", "linkedin", "education", "other_education", "position"])
        writer.writeheader()
        for user in ser.data:
            dictio = {}
            list_user = list(user.items())

            name = list_user[1][1]
            dictio['name'] = name

            email = list_user[2][1]
            dictio['email'] = email
            
            # Profile
            dict_profile = list_user[3][1]
            list_profile = list(dict_profile.items())

            gender = list_profile[2][1]
            if gender == None or gender == "":
                gender = "None"
            dictio['gender'] = gender

            phone = list_profile[3][1]
            if phone == None or phone == "":
                phone = "None"
            dictio['phone'] = phone

            birth_date = list_profile[4][1]
            if birth_date == None or birth_date == "":
                birth_date = "None"
            dictio['birth_date'] = birth_date

            city = list_profile[5][1]
            if city == None or city == "":
                city = "None"
            dictio['city'] = city

            country = list_profile[6][1]
            if country == None or country == "":
                country = "None"
            dictio['country'] = country

            linkedin = list_profile[10][1]
            if linkedin == None or linkedin == "":
                linkedin = "None"
            dictio['linkedin'] = linkedin

            # Education
            dict_edu = list_user[4][1]
            list_edu = []
            for edu in dict_edu:
                edu_map = {}
                edu_obj = list(edu.items())

                npm = edu_obj[3][1]
                if npm == None or npm == "":
                    npm = "None"
                edu_map['npm'] = npm

                class_year = edu_obj[4][1]
                if class_year == None or class_year == "":
                    class_year = "None"
                edu_map['class_year'] = class_year

                class_program = edu_obj[5][1]
                if class_program == None or class_program == "":
                    class_program = "None"
                edu_map['class_program'] = class_program

                status = edu_obj[6][1]
                if status == None or status == "":
                    status = "None"
                edu_map['status'] = status

                grad_year = edu_obj[7][1]
                if grad_year == None or grad_year == "":
                    grad_year = "None"
                edu_map['grad_year'] = grad_year
                
                term_grad = edu_obj[8][1]
                if term_grad == None or term_grad == "":
                    term_grad = "None"
                edu_map['term_grad'] = term_grad

                list_edu.append(edu_map)
            
            dictio['education'] = list_edu

            # Other Education
            dict_other_edu = list_user[5][1]
            list_other_edu = []
            for other_edu in dict_other_edu:
                other_edu_map = {}
                other_edu_obj = list(other_edu.items())

                country = other_edu_obj[2][1]
                if country == None or country == "":
                    country = "None"
                other_edu_map['country'] = country

                university = other_edu_obj[3][1]
                if university == None or university == "":
                    university = "None"
                other_edu_map['university'] = university

                program = other_edu_obj[4][1]
                if program == None or program == "":
                    program = "None"
                other_edu_map['program'] = program

                degree = other_edu_obj[5][1]
                if degree == None or degree == "":
                    degree = "None"
                other_edu_map['degree'] = degree

                class_year = other_edu_obj[6][1]
                if class_year == None or class_year == "":
                    class_year = "None"
                other_edu_map['class_year'] = class_year

                list_other_edu.append(other_edu_map)
            
            dictio['other_education'] = list_other_edu

            # Position
            dict_position = list_user[6][1]
            list_pos = []
            for pos in dict_position:
                pos_map = {}
                pos_obj = list(pos.items())

                is_current = pos_obj[2][1]
                if is_current == None or is_current == "":
                    is_current = "None"
                pos_map['is_current'] = is_current

                title = pos_obj[4][1]
                if title == None or title == "":
                    title = "None"
                pos_map['title'] = title

                company = pos_obj[5][1]
                if company == None or company == "":
                    company = "None"
                pos_map['company'] = company

                date_started = pos_obj[7][1]
                if date_started == None or date_started == "":
                    date_started = "None"
                pos_map['date_started'] = date_started

                date_ended = pos_obj[8][1]
                if date_ended == None or date_ended == "":
                    date_ended = "None"
                pos_map['date_ended'] = date_ended

                list_pos.append(pos_map)
            
            dictio['position'] = list_pos

            # Write to CSV
            writer.writerow(dictio)
        
        return response
