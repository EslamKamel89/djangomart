from django import forms
from django.contrib.auth.models import User


def clean_email(form: forms.ModelForm, update: bool = False):
    email = form.cleaned_data.get("email")
    if email is None:
        raise forms.ValidationError("Email is required")
    if len(email) >= 350:
        raise forms.ValidationError("Email is too long")
    if (
        User.objects.filter(email=email)
        .exclude(pk=form.instance.pk if update else None)
        .exists()
    ):
        raise forms.ValidationError("Email is taken")

    return email
