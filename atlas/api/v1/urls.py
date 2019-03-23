from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from atlas.api.v1.views import general
from atlas.api.v1.views import account
from atlas.api.v1.views import experience
from atlas.api.v1.views import contact

general = [
    path('/', general.api_v1, name='general-v1'),
]

auth = [
    path('/tokens', account.UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('/tokens/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]

account = [
    path('/register', account.UserCreateView.as_view(), name='account_register'),
    path('/users/<pk>', account.UserDetailView.as_view(),
         name='account_user_detail'),
    path('/users/<pk>/preference', account.UserPreferenceDetailView.as_view(),
         name='account_preference_detail'),
]

experience = [
    path('/users/<user_id>/positions', experience.PositionListCreateView.as_view(),
         name='experience_position_list_create'),
    path('/users/<user_id>/positions/<pk>', experience.PositionDetailView.as_view(),
         name='experience_position_detail'),

    path('/users/<user_id>/educations', experience.EducationListCreateView.as_view(),
         name='experience_education_list_create'),
    path('/users/<user_id>/educations/<pk>', experience.EducationDetailView.as_view(),
         name='experience_education_detail'),
]

contact = [
     path('/contacts', contact.ContactListView.as_view(), name='contacts_list')
]

urlpatterns = [] + general + auth + account + experience + contact
