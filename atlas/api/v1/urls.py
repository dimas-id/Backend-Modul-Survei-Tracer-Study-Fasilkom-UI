from django.urls import path

from atlas.api.v1.views import general

from atlas.api.v1.views.account import UserDetailView

general = [
    path('', general.api_v1, name='general-v1'),
]

account = [
    path('user', UserDetailView.as_view(), name='account-user-detail')
]


urlpatterns = [] + general + account
