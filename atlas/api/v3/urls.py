from django.urls import path
from atlas.api.v3.views import general, survei

general = [
    path('/', general.api_v3, name='general-v3'),
]

survei = [
    path('/survei/list', survei.get_list_survei),
    path('/survei/create', survei.register_survei)
]

urlpatterns = [*general, *survei]
