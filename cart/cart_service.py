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
            self.session.modified = True

    @property
    def cart(self) -> dict[str, Any]:
        return self.session.get("cart", {})

    @cart.setter
    def cart(self, new_cart: dict[str, Any]):
        self.session["cart"] = new_cart
        self.session.modified = True

    def add(self, *, product: Product, count: int, increment: bool = False):
        id, title, price, image, brand, category = (
            str(product.id),  # type: ignore
            product.title,
            float(product.price),
            product.image.url,
            product.brand,
            product.category.name if product.category else None,
        )
        cart = self.cart.copy()
        if id in cart:
            if increment:
                cart[id]["count"] += count
            else:
                cart[id]["count"] = count
        else:
            cart[id] = {
                "title": title,
                "price": price,
                "count": count,
                "image": image,
                "brand": brand,
                "category": category,
            }
        self.cart = cart
