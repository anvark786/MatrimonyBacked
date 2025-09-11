import razorpay
from django.conf import settings

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def create_order(amount, currency="INR", receipt=None):
    return razorpay_client.order.create({
        "amount": int(amount * 100),  # Razorpay works in paise
        "currency": currency,
        "receipt": receipt,
        "payment_capture": 1,
    })

def verify_payment_signature(order_id, payment_id, signature):
    params = {
        "razorpay_order_id": order_id,
        "razorpay_payment_id": payment_id,
        "razorpay_signature": signature,
    }
    return razorpay_client.utility.verify_payment_signature(params)
