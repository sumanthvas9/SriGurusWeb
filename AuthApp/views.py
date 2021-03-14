from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from . import models, forms
from .custom import library


# Create your views here.

# def ap_ae_user_registration_view(request):
#     if request.method == "POST":
#         print(request.POST)
#         form = forms.auth_user_registration_form(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("aexecution:ae_cust_home")
#         else:
#             print(form.errors)
#     else:
#         form = forms.auth_user_registration_form()
#     context_object = {"form": form}
#     return render(request, "AExecution/ae_register.html", context_object)


def ap_ae_logout_view(request):
    logout(request)
    return redirect("aexecution:ae_cust_login")


def auth_user_login_view(request):
    if request.method == "POST":
        form = forms.AuthUserLoginForm(request.POST)
        if form.is_valid():
            logout(request)
            login_id = request.POST.get("login_id")
            login_password = request.POST.get("login_password")
            user = authenticate(username=login_id, password=login_password)
            # request.session.set_expiry(10) ## sets the exp. value of the session
            login(request, user)
            library.delete_sessions_for_user(request.user, all=True)
            nav_url = request.POST.get("next", False)
            if nav_url:
                return HttpResponseRedirect(nav_url)
            return redirect("authentication:auth_login")
        else:
            print(form.errors)
    else:
        form = forms.AuthUserLoginForm()
    context_object = {"form": form}
    return render(request, "AuthApp/ae_login.html", context=context_object)
