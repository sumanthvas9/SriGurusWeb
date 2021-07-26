"""SriGurus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, re_path
    2. Add a URL to urlpatterns:  re_path('blog/', include('blog.urls'))
"""
from django.contrib.auth import get_user_model
from django.urls import re_path, include, re_path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "authentication_api"

router = DefaultRouter()
router.register("my_profile", views.GetUserInfo, basename=get_user_model())

urlpatterns = [
    re_path("", include(router.urls)),
    re_path(r"auth/eregister", views.customer_registration_email, name="api_registration_email"),
    re_path(r"auth/sregister", views.customer_registration_sms, name="api_registration_sms"),
    re_path(r"auth/login", views.customer_login, name="api_login"),
    re_path(r"auth/social/login", views.customer_social_login, name="api_login"),
    re_path(r"auth/change_password", views.change_password, name="api_ch_pwd"),
    re_path(r"auth/forgot_password", views.forgot_password, name="api_ch_pwd"),
    re_path(r"auth/resend_otp", views.resend_auth_otp, name="api_otp_resend"),
    re_path(r"auth/eotp_verify", views.auth_email_otp_validation, name="api_email_otp_valid"),
    re_path(r"auth/sotp_verify", views.auth_sms_otp_validation, name="api_sms_otp_valid"),
    re_path(r"set_profile", views.set_user_info, name="api_set_profile"),
    re_path(r"get_profile", views.get_user_info, name="api_get_profile"),
    re_path(r"categories", views.get_categories_info, name="api_categories"),
    re_path(r"new_request", views.create_service_request, name="api_create_service_request"),
    re_path(r"my_requests", views.get_submitted_requests, name="api_create_service_request"),
    re_path(r"new_form_request", views.create_service_request_with_form, name="api_create_service_request_with_form"),
]
