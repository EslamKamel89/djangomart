import os
from datetime import datetime
from typing import Any, Optional, TypedDict, cast

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from stripe import Event, StripeClient, Webhook
from stripe.checkout import Session

from payment.models import Order, StripeWebhookEvent


class CheckoutMetadata(TypedDict):
    """
    Immutable business identifiers used to reconcile Stripe objects
    back to Django domain objects via webhooks.
    """

    order_id: str
    user_id: str


class StripeService:
    """
    Stripe integration boundary for DjangoMart.
    """

    _client: StripeClient | None = None
    _currency: str | None = None

    # -------------------------
    # Core infrastructure
    # -------------------------

    @classmethod
    def get_client(cls) -> StripeClient:
        """
        Lazily initialize and return a StripeClient instance.

        StripeClient is process-wide and safe to reuse.
        """
        if cls._client is not None:
            return cls._client

        secret_key = os.getenv("STRIPE_SECRET_KEY")
        if not secret_key:
            raise RuntimeError("STRIPE_SECRET_KEY is not set")

        cls._client = StripeClient(secret_key)
        return cls._client

    @classmethod
    def get_currency(cls) -> str:
        """
        Return the application currency in lowercase ISO format.

        Currency is treated as deployment configuration, not request data.
        """
        if cls._currency is not None:
            return cls._currency

        cls._currency = os.getenv("CURRENCY", "USD").lower()
        return cls._currency

    # -------------------------
    # Checkout (PaymentIntent owned by Stripe)
    # -------------------------

    @classmethod
    def create_checkout_session(
        cls,
        *,
        price_in_cents: int,
        success_url: str,
        cancel_url: str,
        metadata: CheckoutMetadata,
    ) -> Session:
        """
        Create a Stripe Checkout Session.

        Stripe Checkout will:
        - Create the PaymentIntent internally
        - Manage authentication and retries
        - Emit webhook events representing payment truth

        Django responsibilities:
        - Provide immutable business metadata (order_id)
        - Never assume success from redirects
        """
        client = cls.get_client()
        session = client.v1.checkout.sessions.create(
            params={
                "mode": "payment",
                "line_items": [
                    {
                        "price_data": {
                            "currency": cls.get_currency(),
                            "product_data": {"name": f"Order #{metadata['order_id']}"},
                            "unit_amount": price_in_cents,
                        },
                        "quantity": 1,
                    }
                ],
                "success_url": success_url,
                "cancel_url": cancel_url,
                "metadata": cast(dict, metadata),
                "payment_intent_data": {"metadata": cast(dict, metadata)},
            }
        )
        return session

    # -------------------------
    # Webhooks (authoritative truth)
    # -------------------------

    @classmethod
    def verify_webhook_event(
        cls,
        *,
        payload: bytes,
        sig_header: str,
        webhook_secret: str | None,
    ):
        """
        Verify and construct a Stripe webhook event.

        Webhooks are the ONLY authoritative source of payment truth.
        Redirects, sessions, and client signals must never be trusted.
        sig_header: Comes from HTTP header: Stripe-Signature
        """
        if not webhook_secret:
            raise RuntimeError("STRIPE_WEBHOOK_SECRET is not configured")
        event = Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=webhook_secret,
        )
        return event

    @classmethod
    def get_order_and_user_from_event(
        cls, event: Event
    ) -> tuple[Optional[User], Optional[Order]]:
        """
        Extract Order and optional User from a Stripe event.

        This method must be defensive:
        - Metadata may be missing
        - order_id may be invalid
        - Order may not exist
        """
        obj: dict[str, Any] = event.data.object
        metadata = obj.get("metadata", {})
        order_id_raw = metadata.get("order_id")
        if not order_id_raw:
            return (None, None)
        try:
            order_id = int(order_id_raw)
        except (TypeError, ValueError):
            return (None, None)

        order: Order | None = Order.objects.filter(id=order_id).first()

        user_id_raw = metadata.get("user_id")
        if not user_id_raw:
            return (None, order)
        try:
            user_id = int(user_id_raw)
        except (TypeError, ValueError):
            return (None, order)

        user = User.objects.filter(id=user_id).first()
        return (user, order)

    @classmethod
    def create_webhook_event_model(cls, event: Event) -> StripeWebhookEvent | None:
        try:
            user, order = cls.get_order_and_user_from_event(event)
            return StripeWebhookEvent.objects.create(
                event_id=event.id,
                stripe_event_type=event.type,
                stripe_metadata=event.data.object.get("metadata", {}),
                payload_snapshot=event.to_dict(),
                stripe_created_at=timezone.make_aware(
                    datetime.fromtimestamp(event.created)
                ),
                order=order,
            )
        except IntegrityError:
            # Event already processed (unique constraint hit)
            return None

    @classmethod
    def handle_payment_succeeded(cls, event: Event):
        user, order = cls.get_order_and_user_from_event(event)
        if not order:
            return
        order = Order.objects.select_for_update().filter(id=order.id).first()
        if not order:
            return
        if order.status != Order.OrderStatus.pending:
            return
        order.status = Order.OrderStatus.paid
        order.save(update_fields=["status"])

    @classmethod
    def handle_payment_failed(cls, event: Event):
        user, order = cls.get_order_and_user_from_event(event)
        if not order:
            return
        order = Order.objects.select_for_update().filter(id=order.id).first()
        if not order:
            return
        if order.status != Order.OrderStatus.pending:
            return
        order.status = Order.OrderStatus.failed
        order.save(update_fields=["status"])
