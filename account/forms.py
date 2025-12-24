from typing import Any

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email is None:
            raise forms.ValidationError("Email is required")
        if User.objects.filter(email == email).exists():
            raise forms.ValidationError("Email is taken")
        if len(email) >= 350:
            raise forms.ValidationError("Email is too long")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
