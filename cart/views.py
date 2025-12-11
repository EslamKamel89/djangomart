from typing import Any

from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, View


class CartShowCreateView(View):
    def get(self, request: HttpRequest):
        return render(request, "cart/cart-summary.html")

    def post(self, request: HttpRequest):
        return JsonResponse({"message": "success"})


class CartUpdateDeleteView(View):
    def put(self, request: HttpRequest, id: int):
        pass

    def delete(self, request: HttpRequest, id: int):
        pass
