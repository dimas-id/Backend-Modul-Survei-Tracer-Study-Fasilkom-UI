from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)

from atlas.api.v1.views import general

from atlas.api.v1.views.account import (
    UserDetailView, UserCreateView)

general = [
    path('', general.api_v1, name='general-v1'),
]

auth = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]

account = [
    path('register', UserCreateView.as_view(), name='account_register'),
    path('user/<username>', UserDetailView.as_view(), name='account_user_detail'),
]


urlpatterns = [] + general + auth + account
