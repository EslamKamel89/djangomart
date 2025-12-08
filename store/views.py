from typing import Any

from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, View

from store.models import Category, Product


def categories(request: HttpRequest):
    return {"categories": Category.objects.all()}


class HomeView(View):
    def get(self, request: HttpRequest):
        products = Product.objects.select_related("category").all()
        return render(request, "store/home.html", {"products": products})


class ProductView(DetailView):
    template_name = "store/product-details.html"
    model = Product

    def get_queryset(self):
        return Product.objects.select_related("category")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        product: Product = self.get_object()  # type: ignore
        data["related_products"] = Product.objects.filter(category=product.category)[2:]
        print(data["related_products"])
        return data


class CategoryView(DetailView):
    template_name = "store/category-details.html"
    model = Category

    def get_queryset(self) -> QuerySet[Any]:
        return Category.objects.prefetch_related("products")
