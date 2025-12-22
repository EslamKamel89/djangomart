from django import forms
from django.forms.utils import ErrorList
from django.utils.safestring import SafeText

from .models import Category, Product


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].required = True

    def clean_price(self):
        price = self.cleaned_data.get("price", -1)
        if price < 0:
            raise forms.ValidationError("Price must be greater than zero")
        return price

    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={"class": "border p-2 w-full rounded-lg "}),
            "slug": forms.TextInput(attrs={"class": "border p-2 w-full rounded-lg "}),
            "brand": forms.TextInput(attrs={"class": "border p-2 w-full rounded-lg "}),
            "price": forms.NumberInput(
                attrs={"class": "border p-2 w-full rounded-lg "}
            ),
            "image": forms.FileInput(attrs={"class": "border p-2 w-full rounded-lg "}),
            "category": forms.Select(attrs={"class": "border p-2 w-full rounded-lg "}),
            "description": forms.Textarea(
                attrs={"class": "border p-2 w-full rounded-lg", "rows": 4}
            ),
        }
