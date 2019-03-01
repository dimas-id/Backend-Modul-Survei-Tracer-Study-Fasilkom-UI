from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from atlas.api.v1.views import general

from atlas.api.v1.views.account import UserDetailView

general = [
    path('', general.api_v1, name='general-v1'),
]

auth = [
    path('auth/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh')
]

account = [
    path('user', UserDetailView.as_view(), name='account_user_detail')
]


urlpatterns = [] + general + auth + account
