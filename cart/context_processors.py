from django.http import HttpRequest


def get_cart(request: HttpRequest):
    from cart.cart_service import CartService

    service = CartService(request)
    return service.cart
