# Default Login View
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password


class AuthUserLoginForm(forms.Form):
    userModel = get_user_model()

    login_id = forms.CharField(required=True, label="Login Id")
    login_id.widget = forms.TextInput(
        attrs={
            "type": "text",
            "class": "form-control",
            "placeholder": "Login Id",
            "required": "true",
        }
    )
    login_password = forms.CharField(required=True, label="Password")
    login_password.widget = forms.PasswordInput(
        attrs={
            "type": "password",
            "class": "form-control",
            "placeholder": "Password",
            "required": "true",
        }
    )

    login_check = False
    login_user = ""
    login_pwd = ""

    def clean(self):
        login_data = self.cleaned_data.get("login_id")
        password_data = self.cleaned_data.get("login_password")
        try:
            base_user = self.userModel.objects.get(username=login_data)
            if not check_password(password_data, base_user.password):
                raise forms.ValidationError("Please provide valid login details")
        except self.userModel.DoesNotExist:
            raise forms.ValidationError("User does not exist")
        except IndexError:
            raise forms.ValidationError("Please provide valid login details")

        return super(AuthUserLoginForm, self).clean()
