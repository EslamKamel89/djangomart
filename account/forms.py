from typing import Any

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

INPUT_STYLES = (
    "block w-full rounded-md border border-gray-300 px-3 py-2 "
    "focus:border-indigo-500 focus:ring-indigo-500"
)

PASSWORD_STYLES = INPUT_STYLES

SUBMIT_STYLES = (
    "w-full bg-primary text-white font-semibold py-2 rounded-md "
    "hover:bg-primary/90 transition"
)


class CreateUserForm(UserCreationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.form_class = "space-y-4 max-w-lg mx-auto"
        self.helper.layout = Layout(
            Field("username", css_class=INPUT_STYLES),
            Field("email", css_class=INPUT_STYLES),
            Div(
                Field("password1", css_class=PASSWORD_STYLES),
                Field("password2", css_class=PASSWORD_STYLES),
                css_class="grid gap-4 md:grid-cols-2",
            ),
            Submit("submit", "Create Account", css_class=SUBMIT_STYLES),
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
