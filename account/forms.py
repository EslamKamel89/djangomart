from typing import Any

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.form_class = "space-y-4"
        self.helper.layout = Layout(
            Field(
                "username",
                css_class="block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-indigo-500 focus:ring-indigo-500",
            ),
            Field(
                "email",
                css_class="block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-indigo-500 focus:ring-indigo-500",
            ),
            Div(
                Field(
                    "password1",
                    css_class="block w-full rounded-md border border-gray-300 px-3 py-2",
                ),
                Field(
                    "password2",
                    css_class="block w-full rounded-md border border-gray-300 px-3 py-2",
                ),
                css_class="space-y-4",
            ),
            Submit(
                "submit",
                "Create Account",
                css_class="w-full bg-primary text-white font-semibold py-2 rounded-md",
            ),
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email is None:
            raise forms.ValidationError("Email is required")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is taken")
        if len(email) >= 350:
            raise forms.ValidationError("Email is too long")
        return email

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
