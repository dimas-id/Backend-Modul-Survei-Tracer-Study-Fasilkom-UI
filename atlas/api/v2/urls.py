from django.urls import path

from atlas.api.v2.views import general
from atlas.api.v2.views import account

general = [
    path('/', general.api_v2, name='general-v2'),
]

account = [
    path('/register', account.UserCreateView.as_view(), name='account_register_v2'),
]

urlpatterns = [*general, *account]
