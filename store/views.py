from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, View

from store.models import Category


class HomeView(View):
    def get(self, request: HttpRequest):
        categories = Category.objects.all()
        return render(request, "store/home.html", {"categories": categories})
