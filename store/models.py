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
