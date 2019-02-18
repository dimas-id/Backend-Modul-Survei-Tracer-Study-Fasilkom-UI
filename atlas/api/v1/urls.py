from django.urls import path

from atlas.api.v1.views import general

from atlas.api.v1.views.account import LoginView
from atlas.api.v1.views.account import LogoutView
from atlas.api.v1.views.account import AccountDetailView
from atlas.api.v1.views.account import TokenView

general = [
    path('', general.api_v1, name='general-view'),
]

account = [
    path('auth/login', LoginView.as_view(), name='auth-login'),
    path('auth/logout', LogoutView.as_view(), name='auth-logout'),
    path('auth/token', TokenView.as_view(), name='auth-session'),
    path('account', AccountDetailView.as_view(), name='account-account-detail')
]


urlpatterns = [] + general + account 
