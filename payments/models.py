from django.db import models
from matrimony.models import BaseModel
from users.models import User

class Plan(BaseModel):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20, unique=True, help_text="Unique code for the plan")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - ₹{self.price}"

class PaymentOrder(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey("Plan", on_delete=models.SET_NULL, null=True, blank=True)
    order_id = models.CharField(max_length=100, unique=True)  # Razorpay Order ID
    receipt = models.CharField(max_length=100, unique=True, null=True, blank=True)  # Razorpay receipt identifier
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="INR")
    status = models.CharField(max_length=20, choices=[
        ("created", "Created"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ], default="created")
    

class Payment(BaseModel):
    order = models.ForeignKey(PaymentOrder, on_delete=models.CASCADE, related_name="payments")
    payment_id = models.CharField(max_length=100, unique=True)  # Razorpay Payment ID
    status = models.CharField(max_length=20, choices=[
        ("initiated", "Initiated"),
        ("success", "Success"),
        ("failed", "Failed"),
    ])
    method = models.CharField(max_length=50, null=True, blank=True)  # UPI, Card, NetBanking
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    captured = models.BooleanField(default=False)  # Razorpay capture status


class Refund(BaseModel):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="refunds")
    refund_id = models.CharField(max_length=100, unique=True)  # Razorpay Refund ID
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ("initiated", "Initiated"),
        ("processed", "Processed"),
        ("failed", "Failed"),
    ], default="initiated")
    reason = models.TextField(null=True, blank=True)


