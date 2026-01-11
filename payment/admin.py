from django.contrib import admin

from payment.models import ShippingAddress


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "email",
        "city",
        "state",
        "zipcode",
        "user",
    )
    list_display_links = ("full_name", "email")
    list_filter = ("city", "state")
    search_fields = ("full_name", "email", "city", "state", "zipcode")
    ordering = ("full_name", "email", "city", "state", "zipcode")
