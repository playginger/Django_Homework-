import stripe
from django.conf import settings


def create_payment(payment_amount):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    response = stripe.PaymentIntent.create(
        amount=payment_amount,
        currency="usd",
        automatic_payment_methods={"enabled": True},
    )
    print("response")
    return response['id']
