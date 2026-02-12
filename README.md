# 🛒 DjangoMart — A Stripe-Driven, Event-Safe eCommerce Core

> A white-label eCommerce backend engineered for real-world payment systems.
> Built to survive retries, race conditions, webhook storms, and bad network days.

---

## 🧠 What Is This Project?

DjangoMart is a Django-based eCommerce backend designed around one principle:

> Payments are asynchronous distributed systems — not button clicks.

This project integrates **Stripe Checkout** correctly and safely, using:

- Webhook-driven truth
- Event-level idempotency
- Transactional row locking
- State-machine modeling
- Replay protection
- Audit persistence

You can add your brand, plug in your frontend, and ship.

The payment engine is already built like it expects money to be involved.

---

# 🏗️ Architecture Overview

## Stripe Checkout Ownership Model

- Stripe owns PaymentIntent creation.
- Django never manually creates PaymentIntents in Checkout mode.
- Webhooks are the only authoritative source of payment truth.
- Redirects are UI sugar.

This follows Stripe’s intended orchestration model — not StackOverflow copy-paste patterns.

---

## Payment Lifecycle (Actual Flow)

```
User → Checkout → Stripe → Webhook → Django → Order State Transition
```

Detailed sequence:

1. Order created in `pending`
2. Stripe Checkout Session created
3. Stripe creates PaymentIntent internally
4. User completes authentication (or not)
5. Stripe emits signed webhook event
6. Event is verified cryptographically
7. Event is persisted (idempotency layer)
8. Order state transitions atomically
9. System remains consistent under retries

No redirect-based guessing.
No optimistic state changes.

---

# 🔐 Security Model

### 1️⃣ Signature Verification

Every webhook request is:

- Verified using Stripe’s `Webhook.construct_event`
- Rejected if signature invalid
- CSRF exempted intentionally (server-to-server trust)

No signature = no mutation.

---

### 2️⃣ Event-Level Idempotency (Database-Enforced)

Each Stripe event:

```python
event_id = models.CharField(unique=True)
```

This guarantees:

- Replay protection
- Retry safety
- Duplicate delivery tolerance

If Stripe retries the same event:

- Database rejects duplicate
- System returns 200
- Nothing explodes

Because Stripe _will_ retry.

---

### 3️⃣ Transactional Integrity

Order state mutations:

```python
with transaction.atomic():
    Order.objects.select_for_update()
```

This ensures:

- Row-level locking
- Race condition prevention
- Horizontal scaling safety
- Multi-worker correctness

Two webhooks hitting at the same millisecond?
Only one wins the lock. The other backs off politely.

---

# 📦 Order State Machine

Explicit finite states:

- `pending`
- `paid`
- `failed`

Transitions allowed:

- `pending → paid`
- `pending → failed`

Disallowed:

- `paid → pending`
- `failed → paid`
- Chaos

State checks happen **inside the transaction lock**, not before it.

Idempotency is enforced both:

- At the Order state layer
- At the Stripe event layer

This is how you make double-processing mathematically difficult.

---

# 📊 Webhook Audit Trail

Every Stripe event is stored with:

- `event_id`
- `stripe_event_type`
- Full `payload_snapshot`
- `stripe_metadata`
- `stripe_created_at`
- `processed_successfully`
- Linked `Order`

Why?

Because production debugging exists.

If something weird happens in production, you can:

- Inspect the raw payload
- Replay locally
- Trace event ordering
- Verify processing status

It’s not “it worked.”
It’s “here’s the proof.”

---

# ⚙️ Event Routing Strategy

Only final financial events mutate state:

- `payment_intent.succeeded`
- `payment_intent.payment_failed`
- `checkout.session.expired`

We intentionally ignore:

- Transitional noise
- UI completion signals
- Non-final states

Stripe decides what happened.
Django decides what to do about it.

---

# 🧪 Edge Cases Explicitly Handled

- Duplicate webhook delivery
- Out-of-order events
- Expired Checkout sessions
- Missing metadata
- Invalid Order references
- Stripe retry storms
- Multi-process concurrency
- Crash between event record and state mutation

If something can happen in distributed systems, it was considered.

---

# 🏷️ White-Label Ready

This project is intentionally:

- Backend-focused
- Brand-neutral
- Theme-agnostic

To ship:

1. Add your frontend (React/Vue/Nuxt/Flutter/etc.)
2. Add visual identity
3. Configure Stripe keys
4. Deploy

No payment refactoring required.

---

# 🛠️ Tech Stack

- Django 5
- Stripe Python SDK (StripeClient v8+)
- JSONField-based payload persistence
- Transaction-safe ORM operations
- Django Admin observability layer

PostgreSQL-ready. Horizontal scaling-safe.

---

# 🧩 Why This Isn’t a Tutorial Clone

Most Stripe examples:

- Trust success URLs ❌
- Don’t store event IDs ❌
- Skip concurrency safety ❌
- Ignore retries ❌
- Don’t model state ❌

This project:

- Treats payments as distributed systems
- Models state transitions explicitly
- Stores raw events
- Locks rows correctly
- Enforces idempotency at two layers

This is infrastructure, not a demo.

---

# 🧑‍💼 What This Signals to Recruiters

This project demonstrates:

- Deep understanding of Stripe’s architecture
- Event-driven backend design
- Idempotency in real systems
- Database-level guarantees
- Concurrency control
- Defensive programming
- Production thinking

It’s not:

> “I integrated Stripe.”

It’s:

> “I built a payment system that behaves correctly under failure.”

---

# 🧠 Engineering Philosophy

Money systems must assume:

- Retries
- Partial failures
- Out-of-order events
- Network instability
- Concurrency

This project was built under those assumptions.

Because production is not localhost.

---

# 📈 Extension-Ready

Future enhancements can include:

- Fulfillment pipelines
- Inventory locking
- Refund & dispute handling
- Subscription engine
- Multi-tenant merchant mode
- Background job processing

The core payment layer already supports these safely.

---

# 💬 Final Note

This project does not try to impress with CSS.

It tries to impress distributed systems.

If you’ve ever debugged a payment bug at 2 AM,
you’ll appreciate this architecture.
