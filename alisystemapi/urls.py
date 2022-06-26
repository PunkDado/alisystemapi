"""alisystemapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path, include
from myapp.views import LoginApiView
from myapp.views import UsuarioApiView, UsuarioIdApiView
from myapp.views import RegisterAPI

from knox import views as knox_views
from myapp.views import LoginAPI
from django.urls import path

#from myapp.views import login_user
#from alisystemapi import urls as alisystem_urls

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/register/', RegisterAPI.as_view(), name='register'),

    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

    path('usuarios/', UsuarioApiView.as_view()),
    path('usuarios/<int:id>', UsuarioIdApiView.as_view()),
    path('login/', LoginApiView.as_view()),
]
