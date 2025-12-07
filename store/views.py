from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, View

from store.models import Category, Product


def categories(request: HttpRequest):
    return {"categories": Category.objects.all()}


class HomeView(View):
    def get(self, request: HttpRequest):
        products = Product.objects.select_related("category").all()
        return render(request, "store/home.html", {"products": products})
