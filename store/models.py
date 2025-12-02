from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100 , null=False , unique=True , db_index=True)
    slug = models.SlugField(max_length=255 , unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name.capitalize()}"
    class Meta :
        verbose_name_plural = 'categories'

class Product(models.Model):
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=255 , default='un-branded')
    description = models.TextField(blank=True , null=True)
    slug = models.SlugField(max_length=255 , unique=True)
    price = models.DecimalField(max_digits=8 , decimal_places=2 )
    image = models.ImageField(upload_to='images/')

    def __str__(self) -> str:
        return f"{self.title} - (${self.price})"

