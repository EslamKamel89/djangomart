from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html

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
    list_display = ("id", "title", "slug", "brand", "price", "image_thumbnail")
    list_display_links = ("title", "slug")
    list_editable = ("brand",)
    list_filter = ("brand",)
    search_fields = ("title", "slug", "brand")
    ordering = ("-created_at",)
    prepopulated_fields = {"slug": ("title",)}
    list_per_page = 20
    readonly_fields = ("image_thumbnail",)
    actions = ("make_price_zero",)

    fieldsets = (
        (None, {"fields": ("title", "slug")}),
        ("Information", {"fields": ("price", "description")}),
    )

    def image_thumbnail(self, obj: Product):
        if not obj.image:
            return "no image"
        return format_html(
            '<img src="{}" style="height:40px; width:40px; object-fit:cover; border-radius:6px; display:block;"/>',
            obj.image.url,
        )

    @admin.action(description="Update the prices to zero")
    def make_price_zero(self, request: HttpRequest, queryset: QuerySet):
        updated = queryset.update(price=0)
        self.message_user(request, f"{updated} product(s) updated.")
