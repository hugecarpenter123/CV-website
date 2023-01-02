from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "login-input"
            }
        )
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "login-input"
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username__iexact=username)
        if qs.exists():
            print("username.exists()")
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            print("email.exists()")
            raise ValidationError("Email already exists")
        return email

    def clean_password(self):
        pwd1 = self.cleaned_data.get("password")
        pwd2 = self.cleaned_data.get("password2")
        if pwd1 != pwd2:
            raise ValidationError("Passwords must be the same")

class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "login-input"
            }
        )
    )
    
    def clean_email(self):
        login = self.cleaned_data.get('login')
        qs_username = User.objects.filter(username__iexact=login)
        qs_email = User.objects.filter(username__iexact=login)

        if qs_email.exists():
            return qs_email
        elif qs_username.exists():
            return qs_username

