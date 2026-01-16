from django.contrib import admin

from payment.models import Order, OrderItem, ShippingAddress


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
    read_only_fields = ("id", "created_at")
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
            {"fields": ("amount_paid",)},
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
