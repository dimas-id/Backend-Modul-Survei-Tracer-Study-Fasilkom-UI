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
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include as __include__
from django.views.generic import RedirectView
from rest_framework.documentation import include_docs_urls

from atlas.admin import admin_site
from atlas.libs.utils.urls import includer

include = includer('atlas')

urlpatterns = i18n_patterns(path('__admin__/', admin_site.urls)) + \
              [
                  path('jet/', __include__('jet.urls', 'jet')),  # Django JET URLS
                  path('jet/dashboard/', __include__('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
                  path('__admin__/', RedirectView.as_view(url='/id/__admin__/', permanent=True), name='redirect_admin'),
                  path('__docs__/', include_docs_urls(title='Atlas API')),
                  path('__rq__/', __include__('django_rq.urls')),
                  path('api', include('api')),
              ]
