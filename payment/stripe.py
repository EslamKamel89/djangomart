import os
from typing import cast

from stripe import StripeClient

from payment.types import PaymentIntentMetadata


class StripeService:
    _client: StripeClient | None = None
    _currency: str | None = None

    @classmethod
    def get_client(cls) -> StripeClient:
        if cls._client is not None:
            return cls._client
        secret_key = os.getenv("STRIPE_SECRET_KEY")
        if not secret_key:
            raise RuntimeError("STRIPE_SECRET_KEY is not set")
        cls._client = StripeClient(secret_key)
        return cls._client

    @classmethod
    def get_currency(cls):
        if cls._currency is not None:
            return cls._currency
        cls._currency = os.getenv("CURRENCY", "USD")
        return cls._currency

    @classmethod
    def create_payment_intent(
        cls,
        *,
        amount: int,
        metadata: PaymentIntentMetadata,
    ):
        """
        Create a Stripe PaymentIntent.

        This represents an attempt to move money.
        Does NOT confirm or capture payment.
        """
        client = cls.get_client()
        payment_intent = client.v1.payment_intents.create(
            params={
                "amount": amount,
                "currency": cls.get_currency().lower(),
                "metadata": cast(dict[str, str], metadata),
            },
            options={"idempotency_key": f"payment_intent:order:{metadata['order_id']}"},
        )
        return payment_intent

    @classmethod
    def retrieve_payment_intent(
        cls,
        *,
        payment_intent_id: str,
    ) -> None:
        """
        Retrieve an existing PaymentIntent from Stripe.
        """
        pass

    @classmethod
    def create_checkout_session(
        cls,
        *,
        payment_intent_id: str,
        success_url: str,
        cancel_url: str,
    ) -> None:
        """
        Create a Stripe Checkout Session tied to an existing PaymentIntent.
        """
        pass

    @classmethod
    def verify_webhook_event(
        cls,
        *,
        payload: bytes,
        sig_header: str,
        webhook_secret: str,
    ) -> None:
        """
        Verify and construct a Stripe webhook event.
        """
        pass
