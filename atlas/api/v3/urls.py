from django.urls import path
from atlas.api.v3.views import general, survei, pertanyaan

general = [
    path('/', general.api_v3, name='general-v3'),
]

survei = [
    path('/survei/list', survei.get_list_survei),
    path('/survei/create', survei.register_survei),
    path('/pertanyaan/create/skala-linier', pertanyaan.register_skala_linier),
]

urlpatterns = [*general, *survei]
