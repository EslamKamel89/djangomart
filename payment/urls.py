from django.urls import URLPattern, path

from . import views

urlpatterns: list[URLPattern] = [
    path("/checkout", views.CheckoutView.as_view(), name="checkout"),
    path("success", views.PaymentSuccess.as_view(), name="payment-success"),
    path("failure", views.PaymentFailure.as_view(), name="payment-failure"),
]
