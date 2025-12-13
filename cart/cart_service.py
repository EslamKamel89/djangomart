from decimal import Decimal
from typing import Any

from django.http import HttpRequest

from store.models import Product


class CartService:
    def __init__(self, request: HttpRequest) -> None:
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            self.session["cart"] = {}

    @property
    def cart(self) -> dict[str, Any]:
        return self.session.get("cart", {})

    @cart.setter
    def cart(self, new_cart: dict[str, Any]):
        self.session["cart"] = new_cart

    def add(self, *, product: Product, count: int):
        id, title, price = str(product.id), product.title, product.price  # type: ignore
        cart = self.cart.copy()
        if id in cart:
            cart[id]["count"] += 1
        else:
            cart[id] = {"title": title, "price": price, "count": count}
        self.cart = cart
