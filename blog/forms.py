from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class ContactForm(forms.Form):
    name = forms.CharField(label="Ім'я", max_length=100, required=True,
                           widget=forms.TextInput(attrs={"class": "form-control",
                                                         "placeholder": "Введіть ваше ім'я..."}))
    email = forms.EmailField(label="Електронна пошта", required=True,
                             widget=forms.EmailInput(attrs={"class": "form-control",
                                                            "placeholder": "Введіть електронну пошту..."}))
    phone = forms.CharField(label="Номер телефону", max_length=20, required=True,
                            widget=forms.TextInput(attrs={"class": "form-control",
                                                          "placeholder": "Введіть ваш номер телефону..."}))
    message = forms.CharField(label="Питання", required=True,
                              widget=forms.Textarea(attrs={"class": "form-control",
                                                           "placeholder": "Введіть ваше питання тут"}))


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Нікнейм",
        widget=forms.TextInput(
            attrs={"class": "form-control",
                   "placeholder": "Введіть ваш нік..."}))
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control",
                   "placeholder": "Введіть ваш пароль..."}))

