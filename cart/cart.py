from typing import Any

from django.http import HttpRequest


class Cart:
    def __init__(self, request: HttpRequest) -> None:
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            self.session["cart"] = {}

    @property
    def cart(self):
        return self.session.get("cart")

    @cart.setter
    def cart(self, new_cart: Any):
        self.session["cart"] = new_cart
