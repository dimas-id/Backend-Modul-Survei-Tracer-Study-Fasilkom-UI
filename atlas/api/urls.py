from django.urls import path
from atlas.libs.utils.urls import includer

include = includer('atlas.api')

urlpatterns = [
    path('/v1', include('v1')),
    path('/v2', include('v2')),
    path('/v3', include('v3'))
]
