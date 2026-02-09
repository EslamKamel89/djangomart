import os

from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from payment.stripe import StripeService


@method_decorator(csrf_exempt, "dispatch")
class StripeWebHookView(View):
    def post(self, request: HttpRequest):
        payload = request.body
        sig_header = request.headers.get("Stripe-Signature")
        webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET")
        if sig_header is None:
            return HttpResponse(status=400)
        try:
            event = StripeService.verify_webhook_event(
                payload=payload,
                sig_header=sig_header,
                webhook_secret=os.environ.get("STRIPE_WEBHOOK_SECRET"),
            )
            print("Webhook received and signature is correct")
            print(event)
            print(event.data)
        except RuntimeError as e:
            print(f"StripeWebHookView.post RuntimeError: {e}")
            # Server misconfigured (missing secret)
            return HttpResponse(status=500)
        except Exception as e:
            print(f"StripeWebHookView.post Exception: {e}")
            # Invalid payload or invalid signature
            return HttpResponse(status=400)
        return HttpResponse(status=200)
