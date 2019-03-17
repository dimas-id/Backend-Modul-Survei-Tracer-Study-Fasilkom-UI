"""atlas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import django_rq

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include as __include__

from rest_framework.documentation import include_docs_urls

from atlas.common.admin import admin_site
from atlas.common.utils.urls import includer

include = includer('atlas')

urlpatterns = [
    path('__admin__', admin_site.urls),
    path('__docs__', include_docs_urls(title='Atlas API')),
    path('__rq__', __include__('django_rq.urls')),
    path('api', include('api')),
]
