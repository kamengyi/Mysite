from django import forms
from .models import User
from captcha.fields import CaptchaField

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=64)
    email = forms.EmailField(max_length=128, widget=forms.EmailInput())
    password1 = forms.CharField(max_length=128, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=128, widget=forms.PasswordInput())
    captcha = CaptchaField()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput())
    captcha = CaptchaField()

