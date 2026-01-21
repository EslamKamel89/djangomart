from decimal import Decimal
from http.client import HTTPException

from django.contrib import messages
from django.contrib.auth.models import User
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

    def get_shipping_address(self, user: User | None):
        return ShippingAddress.objects.filter(user=user).first() if user else None

    def is_cart_empty(self, cart: Cart):
        return len(cart) == 0

    def get(self, request: HttpRequest):
        cart_service = CartService(request)
        cart = cart_service.cart
        user: User | None = request.user if request.user.is_authenticated else None  # type: ignore
        if self.is_cart_empty(cart):
            messages.error(request, "Your cart is empty")
            return redirect("/")
        shipping_address = self.get_shipping_address(user)
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
        user: User | None = request.user if request.user.is_authenticated else None  # type: ignore
        if self.is_cart_empty(cart):
            messages.error(request, "Your cart is empty")
            return redirect("/")
        shipping_address = self.get_shipping_address(user)
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
            shipping_address_obj = form.save(commit=False)
            if shipping_address_obj is None:
                raise HTTPException("Failed to update the shipping address")
            if request.user.is_authenticated:
                shipping_address_obj.user = request.user  # type: ignore
                shipping_address_obj.save()
                messages.success(request, "Shipping address saved successfully")
            shipping_address_text = Order.format_shipping_address(shipping_address_obj)
            order = Order.objects.create(
                full_name=form.cleaned_data.get("full_name"),
                email=form.cleaned_data.get("email"),
                shipping_address=shipping_address_text,
                amount_paid=cart_total,
                user=user,
            )
            # todo: handle the checkout payment flow
            messages.success(request, "Checkout details confirmed successfully")
            return redirect(reverse("payment-success"))


class PaymentSuccess(TemplateView):
    template_name = "payment/payment-success.html"


class PaymentFailure(TemplateView):
    template_name = "payment/payment-failure.html"
