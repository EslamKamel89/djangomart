from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit
from django import forms
from django.contrib.auth.models import User

from account.forms import INPUT_STYLES, SUBMIT_STYLES
from payment.models import ShippingAddress


class ShippingAddressForm(forms.ModelForm):
    def __init__(self, btn_label: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.form_class = "space-y-4 max-w-lg mx-auto"
        self.helper.layout = Layout(
            Field("full_name", css_class=INPUT_STYLES),
            Field("email", css_class=INPUT_STYLES),
            Field("address1", css_class=INPUT_STYLES, rows=3),
            Field("address2", css_class=INPUT_STYLES, rows=3),
            Field("city", css_class=INPUT_STYLES),
            Field("state", css_class=INPUT_STYLES),
            Field("zipcode", css_class=INPUT_STYLES),
            Submit("submit", btn_label, css_class=SUBMIT_STYLES),
        )

    class Meta:
        model = ShippingAddress
        fields = (
            "full_name",
            "email",
            "address1",
            "address2",
            "city",
            "state",
            "zipcode",
        )
        labels = {
            "address1": "Street address",
            "address2": "Apartment, suite, unit (optional)",
        }
