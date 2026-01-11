from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class ShippingAddress(models.Model):
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
