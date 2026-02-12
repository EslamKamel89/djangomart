import os

from django.db import transaction
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
                webhook_secret=webhook_secret,
            )
            print("Webhook received and signature is correct")
            event_type = event.type
            print(f"StripeWebHookView.post webhook event is received: {event_type}")
            with transaction.atomic():
                webhook_event_model = StripeService.create_webhook_event_model(event)
                if not webhook_event_model:
                    return HttpResponse(200)
                match event_type:
                    case "payment_intent.succeeded":
                        StripeService.handle_payment_succeeded(event)
                    case "payment_intent.payment_failed":
                        StripeService.handle_payment_failed(event)
                    case "checkout.session.expired":
                        StripeService.handle_payment_failed(event)
                    case _:
                        print(f"Ignored Stripe event type: {event_type}")
                webhook_event_model.processed_successfully = True
                webhook_event_model.save(update_fields=["processed_successfully"])

        except RuntimeError as e:
            print(f"StripeWebHookView.post RuntimeError: {e}")
            # Server misconfigured (missing secret)
            return HttpResponse(status=500)
        except Exception as e:
            print(f"StripeWebHookView.post Exception: {e}")
            # Invalid payload or invalid signature
            return HttpResponse(status=400)
        return HttpResponse(status=200)
