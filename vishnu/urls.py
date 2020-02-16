"""vishnu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
import os
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .routers import router
from .views import RegistrationAPI, LoginAPI, UserAPI

def add_url_for_path(file_path, urlpatterns, content_type="application/javascript"):
    urlpatterns += [path(
        file_path,
        TemplateView.as_view(template_name=file_path,
                             content_type=content_type),
        name=file_path
    )]

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),

    # Authentication
    path("",
         TemplateView.as_view(template_name="index.html"),
         name="app",
         ),

    path("index.html",
         TemplateView.as_view(template_name="index.html"),
         name="app",
         ),

    path("service-worker.js",
         TemplateView.as_view(template_name="service-worker.js",
                              content_type='application/javascript'),
         name="service-worker",
         ),

    path("manifest.json",
         TemplateView.as_view(template_name="manifest.json",
                              content_type='application/manifest+json'),
         name="manifest-json",
         ),

    path("robots.txt",
         TemplateView.as_view(template_name="robots.txt",
                              content_type='txt/plain'),
         name="robots-txt",
         ),

    path('api/auth/', include('knox.urls')),
    path("api/auth/register", RegistrationAPI.as_view()),
    path("api/auth/login", LoginAPI.as_view()),
    path("api/auth/user", UserAPI.as_view()),
]

for f in os.listdir(os.path.join(settings.FRONTEND_DIR, 'dist')):
    if "precache-manifest" in f:
        add_url_for_path(f, urlpatterns)
# Required to serve static files in prod. Workaround for now
# Use https://pypi.org/project/dj-static/ or other solutions instead in future
urlpatterns += staticfiles_urlpatterns()
