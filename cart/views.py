import json
from typing import Any

from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView, TemplateView, View

from cart.cart_service import CartService
from store.models import Product


class CartShowCreateView(View):
    def get(self, request: HttpRequest):
        return render(request, "cart/cart-summary.html")

    def post(self, request: HttpRequest):
        try:
            body: dict[str, Any] = json.loads(request.body.decode())
        except Exception as e:
            return JsonResponse({"error": "invalid json"}, status=400)
        product_id = body.get("product_id")
        product_id = int(product_id) if product_id else None
        count = body.get("count")
        count = int(count) if count else None
        if not product_id or not count:
            return JsonResponse(
                {"error": "product_id and count are required"}, status=400
            )
        product = get_object_or_404(Product, pk=product_id)
        cart_service = CartService(request)
        cart_service.sync(product=product, count=count)
        return JsonResponse({"cart": cart_service.cart})


class CartDeleteView(View):
    def delete(self, request: HttpRequest, id: int):
        get_object_or_404(Product, pk=id)
        cart_service = CartService(request)
        cart_service.delete(id)
        return JsonResponse({"cart": cart_service.cart})
