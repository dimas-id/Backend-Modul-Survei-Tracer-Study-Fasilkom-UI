from django.urls import path
from atlas.common.utils.urls import includer

include = includer('atlas.api')

urlpatterns = [
    path('v1/', include('v1'))
]
