from django.contrib import admin

from store.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "created_at", "updated_at")
    list_display_links = ("name", "slug")
    list_filter = ("created_at",)
    search_fields = ("name", "slug")
    ordering = ("-created_at",)
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 25
    date_hierarchy = "created_at"
    # readonly_fields = ("id",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
