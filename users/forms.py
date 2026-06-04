from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from users.models import User
from users.validators import validate_github_url, validate_phone_number


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    class Meta:
        model = User
        fields = ["name", "surname", "email", "password"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        validate_password(password)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            self.user = authenticate(
                request=self.request, email=email, password=password
            )
            if not self.user:
                raise forms.ValidationError("Неверный email или пароль")
        return cleaned_data

    def get_user(self):
        return self.user


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Старый пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password2 = forms.CharField(
        label="Подтверждение нового пароля",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )


class ProfileEditForm(forms.ModelForm):
    github_url = forms.URLField(
        required=False, validators=[validate_github_url])
    phone = forms.CharField(required=False, validators=[validate_phone_number])

    class Meta:
        model = User
        fields = [
            "name",
            "surname",
            "avatar",
            "about",
            "phone",
            "github_url",
        ]
