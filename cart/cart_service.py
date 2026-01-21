from decimal import Decimal
from typing import Any

from django.http import HttpRequest

from cart.types import Cart
from store.models import Product


class CartService:
    def __init__(self, request: HttpRequest) -> None:
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            self.session["cart"] = {}
            self.session.modified = True

    @property
    def cart(self) -> Cart:
        return self.session.get("cart", {})

    @cart.setter
    def cart(self, new_cart: Cart):
        self.session["cart"] = new_cart
        self.session.modified = True

    def sync(self, *, product: Product, count: int, increment: bool = False):
        id, title, price, image, brand, category = (
            str(product.id),  # type: ignore
            product.title,
            float(product.price),
            product.image.url,
            product.brand,
            product.category.name if product.category else None,
        )
        cart: Cart = self.cart.copy()
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

    def delete(self, product_id: int):
        id = str(product_id)
        cart: Cart = self.cart.copy()
        if id in cart:
            del cart[id]
            self.cart = cart
            print(cart)

    def get_total(self) -> Decimal:
        return Decimal(
            sum(
                Decimal(str(item["price"])) * item["count"]
                for item in self.cart.values()
            )
        )
