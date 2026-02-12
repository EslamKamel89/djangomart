import json

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from payment.models import Order, OrderItem, ShippingAddress, StripeWebhookEvent


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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "email",
        "amount_paid",
        "user",
        "status",
        "created_at",
    )
    list_display_links = ("id", "full_name")
    list_filter = ("created_at", "user")
    search_fields = (
        "id",
        "full_name",
        "email",
    )
    ordering = ("-created_at",)
    read_only_fields = ("id", "created_at", "status")
    list_per_page = 25
    fieldsets = (
        (
            "Customer Information",
            {
                "fields": (
                    "full_name",
                    "email",
                    "user",
                )
            },
        ),
        (
            "Shipping Snapshot",
            {"fields": ("shipping_address",)},
        ),
        (
            "Order Details",
            {"fields": ("amount_paid", "status")},
        ),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "product",
        "quantity",
        "price",
        "total_price",
    )
    list_display_links = ("id", "order")
    list_filter = (
        "order",
        "product",
    )
    search_fields = (
        "order__id",
        "product__title",
    )
    ordering = ("-id",)
    readonly_fields = ("id",)
    list_per_page = 50

    @admin.display(description="Total Price")
    def total_price(self, obj: OrderItem):
        return f"${(obj.quantity * obj.price):.2f}"


@admin.register(StripeWebhookEvent)
class StripeWebhookEventAdmin(admin.ModelAdmin):

    list_display = (
        "event_id",
        "stripe_event_type",
        "order",
        "processed_successfully",
        "processed_at",
        "stripe_created_at",
    )

    list_filter = (
        "stripe_event_type",
        "processed_successfully",
        "processed_at",
    )

    search_fields = (
        "event_id",
        "order__id",
    )

    readonly_fields = (
        "event_id",
        "order",
        "stripe_metadata",
        "stripe_event_type",
        "pretty_payload",
        "payload_snapshot",
        "processed_successfully",
        "stripe_created_at",
        "processed_at",
    )

    ordering = ("-processed_at",)

    list_select_related = ("order",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def pretty_payload(self, obj):
        formatted = json.dumps(obj.payload_snapshot, indent=2)
        return format_html("<pre>{}</pre>", mark_safe(formatted))
