from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

# Create your views here.


class PaymentSuccess(TemplateView):
    template_name = "payment/payment-success.html"


class PaymentFailure(TemplateView):
    template_name = "payment/payment-failure.html"
