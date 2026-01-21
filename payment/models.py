from typing import TYPE_CHECKING

from django.contrib.auth.models import User
from django.db import models

import store.models as store_models

# Create your models here.


class ShippingAddress(models.Model):
    id: int
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shipping_addresses"
    )
    full_name = models.CharField(max_length=255, db_index=True)
    email = models.EmailField(max_length=255, db_index=True)
    address1 = models.TextField()
    address2 = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, db_index=True)
    state = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    zipcode = models.CharField(max_length=20, null=True, blank=True, db_index=True)

    def __str__(self) -> str:
        return f"{self.full_name} - {self.city}"

    class Meta:
        verbose_name_plural = "Shipping Addresses"
        ordering = ["full_name"]


class Order(models.Model):
    id: int
    full_name = models.CharField(max_length=255, db_index=True)
    email = models.EmailField(max_length=255, db_index=True)
    shipping_address = models.TextField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, related_name="orders"
    )

    def __str__(self) -> str:
        return f"Order #{self.id} - {self.full_name} (${self.amount_paid:.2f})"

    @staticmethod
    def format_shipping_address(obj: ShippingAddress):
        parts = [
            obj.address1,
            obj.address2,
            obj.city,
            obj.state,
            obj.zipcode,
        ]
        return "\n".join([v for v in parts if v and v.strip()])

    class Meta:
        ordering = ["-created_at"]


class OrderItem(models.Model):
    id: int
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(
        store_models.Product,
        on_delete=models.SET_NULL,
        null=True,
        related_name="order_items",
    )
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self) -> str:
        product_name = self.product.title if self.product else "Deleted Product"
        amount_paid = self.quantity * self.price
        return f"Order Item #{self.id} - {product_name} (${amount_paid:.2f})"

    class Meta:
        ordering = ["-created_at"]
