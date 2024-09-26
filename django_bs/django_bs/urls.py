"""
URL configuration for django_bs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
# from app01.views import users
# from django.views.generic.base import TemplateView

# urlpatterns = [
#   path('', TemplateView.as_view(template_name = 'index.html')),
#   path('admin/', admin.site.urls),
#   path('register/', users.register),
#   path('login/', users.login)
# ]

from rest_framework import routers
from app01.views.users import ApiUser
from django.views.generic.base import TemplateView

router = routers.DefaultRouter()
# 第一个参数为url前缀，第二个参数是前缀对应的试图集，第三个参数是视图基本名
router.register('userapi', ApiUser, basename='userapi')

urlpatterns = [
  path('', TemplateView.as_view(template_name='index.html'))
]

urlpatterns += router.urls

