from django.http import HttpRequest
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from cart.cart_service import CartService
from payment.forms import ShippingAddressForm
from payment.models import ShippingAddress

# Create your views here.


class CheckoutView(View):
    def get(self, request: HttpRequest):
        shipping_address: ShippingAddress | None = None
        if request.user.is_authenticated:
            shipping_address = ShippingAddress.objects.filter(user=request.user).first()
        form = ShippingAddressForm(
            btn_label="Complete Order", instance=shipping_address
        )
        cart = CartService(request).cart
        cart_total = sum(item["price"] * item["count"] for item in cart.values())
        return render(
            request, "payment/checkout.html", {"form": form, "cart_total": cart_total}
        )

    def post(self, request: HttpRequest): ...


class PaymentSuccess(TemplateView):
    template_name = "payment/payment-success.html"


class PaymentFailure(TemplateView):
    template_name = "payment/payment-failure.html"
