from decimal import Decimal
from http.client import HTTPException

from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from cart.cart_service import CartService
from cart.types import Cart
from payment.forms import ShippingAddressForm
from payment.models import Order, ShippingAddress

# Create your views here.


class CheckoutView(View):

    def get_shipping_address(self, request: HttpRequest):
        shipping_address: ShippingAddress | None = None
        if request.user.is_authenticated:
            shipping_address = ShippingAddress.objects.filter(user=request.user).first()
        return shipping_address

    def is_cart_empty(self, cart: Cart):
        return len(cart) == 0

    def get(self, request: HttpRequest):
        cart_service = CartService(request)
        cart = cart_service.cart
        if self.is_cart_empty(cart):
            messages.error(request, "Your cart is empty")
            return redirect("/")
        shipping_address = self.get_shipping_address(request)
        form = ShippingAddressForm(
            btn_label="Complete Order", instance=shipping_address
        )
        cart_total = cart_service.get_total()
        return render(
            request, "payment/checkout.html", {"form": form, "cart_total": cart_total}
        )

    def post(self, request: HttpRequest):
        cart_service = CartService(request)
        cart = cart_service.cart
        if self.is_cart_empty(cart):
            messages.error(request, "Your cart is empty")
            return redirect("/")
        shipping_address = self.get_shipping_address(request)
        cart_total = cart_service.get_total()
        form = ShippingAddressForm(
            btn_label="Complete Order", instance=shipping_address, data=request.POST
        )
        if not form.is_valid():
            messages.error(request, "Please fix the validation errors")
            return render(
                request,
                "payment/checkout.html",
                {"form": form, "cart_total": cart_total},
            )
        else:
            shipping_address = form.save(commit=False)
            if shipping_address is None:
                raise HTTPException("Failed to update the shipping address")
            if request.user.is_authenticated:
                shipping_address.user = request.user  # type: ignore
                shipping_address.save()
                messages.success(request, "Shipping address saved successfully")
            shipping_address_text = Order.get_shipping_address(shipping_address)
            # todo: handle the checkout payment flow
            messages.success(request, "Checkout details confirmed successfully")
            return redirect(reverse("payment-success"))


class PaymentSuccess(TemplateView):
    template_name = "payment/payment-success.html"


class PaymentFailure(TemplateView):
    template_name = "payment/payment-failure.html"
