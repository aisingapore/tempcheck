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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .routers import router
from .settings import DEBUG
from .views import RegistrationAPI, LoginAPI, UserAPI, VerifyAPI

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

    path('api/auth/', include('knox.urls')),
    path("api/auth/register", RegistrationAPI.as_view()),
    path("api/auth/login", LoginAPI.as_view()),
    path("api/auth/user", UserAPI.as_view()),
    path("api/auth/verify", VerifyAPI.as_view())
]

if not DEBUG:
    for f in os.listdir('static'):
        if "precache-manifest" in f:
            add_url_for_path(f, urlpatterns)
