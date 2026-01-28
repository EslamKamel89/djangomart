import os

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
if not STRIPE_SECRET_KEY:
    raise RuntimeError("STRIPE_SECRET_KEY is not set")

import stripe

stripe.api_key = STRIPE_SECRET_KEY
