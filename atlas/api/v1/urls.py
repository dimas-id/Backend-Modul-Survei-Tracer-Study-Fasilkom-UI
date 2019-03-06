from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)

from atlas.api.v1.views import general
from atlas.api.v1.views import account
from atlas.api.v1.views import experience

general = [
    path('', general.api_v1, name='general-v1'),
]

auth = [
    path('tokens', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('tokens/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]

account = [
    path('register', account.UserCreateView.as_view(), name='account_register'),
    path('users/<username>', account.UserDetailView.as_view(),
         name='account_user_detail'),
]

experience = [
    path('users/<username>/positions', experience.PositionListCreateView.as_view(),
         name='experience_position_list_create'),
    path('users/<username>/educations', experience.EducationListCreateView.as_view(),
         name='experience_education_list_create')
]

urlpatterns = [] + general + auth + account + experience
