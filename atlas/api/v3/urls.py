from django.urls import path
from atlas.api.v3.views import survei, pertanyaan, response, visualisasi, email_blaster, recipients
from atlas.api.v3.views.email_template import EmailTemplateCreateView, EmailTemplateDeleteView, EmailTemplateListView, EmailTemplateUpdateView

survei = [
    path('/survei/list', survei.get_list_survei),
    path('/survei/create', survei.register_survei),
    path('/survei/delete/', survei.delete_survei_by_id),
    path('/survei/', survei.get_survei_by_id),
    path('/survei/finalize/<str:id>', survei.finalize),
    path('/survei/edit', survei.edit_survei_by_id),
    path('/survei/isi', response.isi_survei),
    path('/pertanyaan/create/skala-linier', pertanyaan.register_skala_linier),
    path('/pertanyaan/create/jawaban-singkat', pertanyaan.register_isian),
    path('/pertanyaan/create/radiobutton', pertanyaan.register_radiobutton),
    path('/pertanyaan/create/dropdown', pertanyaan.register_dropdown),
    path('/pertanyaan/create/checkbox', pertanyaan.register_checkbox),
]

visualisasi = [
    path('/visualisasi/<str:id>', visualisasi.get_visualisasi),
]

email_template = [
    path('/email-templates', EmailTemplateListView.as_view(),
         name='email_templates_list'),
    path('/email-templates/create', EmailTemplateCreateView.as_view(),
         name='email_templates_create'),
    path('/email-templates/<int:pk>', EmailTemplateUpdateView.as_view(),
         name='email_templates_update'),
    path('/email-templates/<int:pk>/delete',
         EmailTemplateDeleteView.as_view(), name='email_templates_delete'),
]

recipients = [
    path('/recipients/csv/upload', recipients.upload_email_csv, name='upload_csv'),
    path('/recipients/get-all', recipients.get_email_recipients, name='get_recipients'),
    path('/recipients/group-total', recipients.get_total_recipients_of_group_email, name='get_group_total'),
]

email_blaster = [
    path('/email-blaster/send', email_blaster.send_email, name='send_email'),
    path('/email-blaster/preview', email_blaster.preview_email, name='preview_email'),
]

urlpatterns = [*survei, *visualisasi, *
               email_template, *recipients, *email_blaster]
