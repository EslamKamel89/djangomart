import os
from typing import Any, TypedDict, cast

from stripe import StripeClient, Webhook
from stripe.checkout import Session


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
