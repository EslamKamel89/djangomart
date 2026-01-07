from typing import Any, Mapping

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
)
from django.contrib.auth.models import User
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList

from helpers.clean_email import clean_email

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
        self.fields["email"].required = True
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
        return clean_email(self, False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = "space-y-4 max-w-lg mx-auto"
        self.helper.layout = Layout(
            Field("username", css_class=INPUT_STYLES),
            Field("password", css_class=PASSWORD_STYLES),
            Submit("submit", "Log in", css_class=SUBMIT_STYLES),
        )


class UpdateUserForm(forms.ModelForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = "space-y-4 max-w-lg mx-auto"
        self.helper.layout = Layout(
            Field("username", css_class=INPUT_STYLES),
            Field("email", css_class=INPUT_STYLES),
            Submit("submit", "Update", css_class=SUBMIT_STYLES),
        )

    def clean_email(self):
        return clean_email(self, True)

    class Meta:
        model = User
        fields = ["username", "email"]


class ResetUserPasswordForm(PasswordChangeForm):
    def __init__(self, user: Any, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = "space-y-4 max-w-lg mx-auto"
        self.helper.layout = Layout(
            Field("old_password", css_class=PASSWORD_STYLES),
            Field("new_password1", css_class=PASSWORD_STYLES),
            Field("new_password2", css_class=PASSWORD_STYLES),
            Submit("submit", "Update Password", css_class=SUBMIT_STYLES),
        )

    class Meta:
        model = User
        fields = ["old_password", "new_password1", "new_password2"]
