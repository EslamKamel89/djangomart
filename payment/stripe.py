import os

from stripe import StripeClient


class StripeService:
    _client: StripeClient | None = None

    currency: str

    def __init__(self) -> None:
        self.currency = os.getenv("CURRENCY", "USD")

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
    def create_payment_intent(
        cls,
        *,
        amount: int,
        metadata: dict[str, str] | None,
    ):
        """
        Create a Stripe PaymentIntent.

        This represents an attempt to move money.
        Does NOT confirm or capture payment.
        """
        pass

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
