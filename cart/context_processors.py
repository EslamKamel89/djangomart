from django.http import HttpRequest

from cart.cart_service import CartService


def get_cart(request: HttpRequest):
    service = CartService(request)
    return {"cart": service.cart}
