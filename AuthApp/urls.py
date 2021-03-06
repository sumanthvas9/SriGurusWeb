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

from django.urls import path, include, re_path

from AuthApp import views

app_name = "authentication"

urlpatterns = [
    # path(r"register", views.ap_ae_user_registration_view, name="auth_register"),
    path(r"login", views.auth_user_login_view, name="auth_login"),
    # path(r"logout", views.ap_ae_logout_view, name="auth_logout"),
]
