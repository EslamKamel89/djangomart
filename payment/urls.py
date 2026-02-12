from django.urls import URLPattern, path

from . import views, webhooks

urlpatterns: list[URLPattern] = [
    path("checkout", views.CheckoutView.as_view(), name="checkout"),
    path("success", views.PaymentSuccess.as_view(), name="payment-success"),
    path("failure", views.PaymentFailure.as_view(), name="payment-failure"),
    path("webhooks", webhooks.StripeWebHookView.as_view(), name="stripe-webhook"),
]
