from typing import Any

from django.contrib import messages
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views.generic import DetailView, View

from store.forms import ProductForm
from store.models import Category, Product


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
        data["product_info"] = {
            "title": product.title,
            "price": product.price,
            "count": 0,
            "image": product.image.url,
            "brand": product.brand,
            "category": product.category.name,  # type: ignore
        }
        return data


class CategoryView(DetailView):
    template_name = "store/category-details.html"
    model = Category

    def get_queryset(self) -> QuerySet[Any]:
        return Category.objects.prefetch_related("products")


class ProductFormView(View):
    template_name = "store/product-form.html"

    def get(self, request: HttpRequest):
        form = ProductForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product created successfully.")
            return redirect("/")
        messages.error(request, "Failed to create product. Please check the form.")
        return render(request, self.template_name, {"form": form})
