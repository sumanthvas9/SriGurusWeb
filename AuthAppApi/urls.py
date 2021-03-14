"""SriGurus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.auth import get_user_model
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "authentication_api"

router = DefaultRouter()
router.register("my_profile", views.GetUserInfo, basename=get_user_model())

urlpatterns = [
    path("", include(router.urls)),
    path(r"auth/register", views.customer_registration, name="api_registration"),
    path(r"auth/login", views.customer_login, name="api_login"),
    path(r"auth/change_password", views.change_password, name="api_ch_pwd"),
    path(r"auth/forgot_password", views.forgot_password, name="api_ch_pwd"),
    path(r"auth/resend_otp", views.resend_auth_otp, name="api_otp_resend"),
    path(r"auth/otp_verify", views.auth_otp_validation, name="api_otp_valid"),
    path(r"set_profile", views.set_user_info, name="api_set_profile"),
    path(r"categories", views.get_categories_info, name="api_categories"),
    path(r"new_request", views.create_service_request, name="api_create_service_request"),
    path(r"my_requests", views.get_submitted_requests, name="api_create_service_request"),

]
