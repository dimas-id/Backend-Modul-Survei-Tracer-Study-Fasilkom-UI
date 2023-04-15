from django.urls import path
from atlas.api.v3.views import survei, pertanyaan, response

survei = [
    path('/survei/list', survei.get_list_survei),
    path('/survei/create', survei.register_survei),
    path('/survei/', survei.get_survei_by_id),
    path('/survei/isi', response.isi_survei),
    path('/pertanyaan/create/skala-linier', pertanyaan.register_skala_linier),
    path('/pertanyaan/create/jawaban-singkat', pertanyaan.register_isian),
    path('/pertanyaan/create/radiobutton', pertanyaan.register_radiobutton),
    path('/pertanyaan/create/dropdown', pertanyaan.register_dropdown),
    path('/pertanyaan/create/checkbox', pertanyaan.register_checkbox),
]

urlpatterns = [*survei]
