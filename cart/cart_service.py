from decimal import Decimal
from typing import Any

from django.http import HttpRequest


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

    def add(self, *, product_id: int, count: int, title: str, price: Decimal):
        pass
