from django.urls import path

from atlas.api.v2.views import general
from atlas.api.v2.views import account
from atlas.api.v2.views import batch
from atlas.api.v2.views import search

general = [
    path('/', general.api_v2, name='general-v2'),
]

account = [
    path('/register', account.UserCreateView.as_view(), name='account_register_v2'),
    path('/users', batch.UserBatchRetrieveView.as_view(), name='batch_retrieve_v2'),
    path('/search', search.UserSearchRetrieveView.as_view(), name='search_retrieve_v2'),
    path('/register-v2', account.BulkUserCreateView.as_view(), name='account_bulk_register_v2'),
    path('/export-csv', account.ExportCSVStudents.as_view(), name='export_csv_v2'),
]

urlpatterns = [*general, *account]
