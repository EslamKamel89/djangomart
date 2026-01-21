from decimal import Decimal
from http.client import HTTPException
from typing import Any

from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from cart.cart_service import CartService
from cart.types import Cart
from payment.forms import ShippingAddressForm
from payment.models import Order, OrderItem, ShippingAddress

# Create your views here.


class CheckoutView(View):

    def get_shipping_address(self, user: User | None):
        return ShippingAddress.objects.filter(user=user).first() if user else None

    def is_cart_empty(self, cart: Cart):
        return len(cart) == 0

    def save_order(
        self,
        user: User | None,
        cart: Cart,
        cleaned_data: dict[str, Any],
        shipping_address_text: str,
        cart_total: Decimal,
    ) -> tuple[Order, list[OrderItem]]:
        if not cart:
            raise ValueError("can not create an order with empty cart")
        with transaction.atomic():
            order = Order.objects.create(
                full_name=cleaned_data["full_name"],
                email=cleaned_data["email"],
                shipping_address=shipping_address_text,
                amount_paid=cart_total,
                user=user,
            )
            items: list[OrderItem] = []
            for product_id, cart_item in cart.items():
                product_id = int(product_id)
                item = OrderItem.objects.create(
                    order=order,
                    product_id=product_id,
                    quantity=cart_item["count"],
                    price=Decimal(str(cart_item["price"])),
                )
                items.append(item)
        return (order, items)

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
        cart_total: Decimal = cart_service.get_total()
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
            if user is not None:
                shipping_address_obj.user = user
                shipping_address_obj.save()
                messages.success(request, "Shipping address saved successfully")
            shipping_address_text = Order.format_shipping_address(shipping_address_obj)
            order, items = self.save_order(
                user, cart, form.cleaned_data, shipping_address_text, cart_total
            )
            # todo: handle the checkout payment flow
            messages.success(request, "Checkout details confirmed successfully")
            return redirect(reverse("payment-success"))


class PaymentSuccess(TemplateView):
    template_name = "payment/payment-success.html"


class PaymentFailure(TemplateView):
    template_name = "payment/payment-failure.html"
