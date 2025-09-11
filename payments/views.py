from datetime import date, timedelta
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import Plan, PaymentOrder, Payment
from .serializers import PlanSerializer
from .services.razorpay_service import create_order, verify_payment_signature
from razorpay.errors import SignatureVerificationError


class PlanListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        plans = Plan.objects.filter(is_active=True)
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        plan_id = request.data.get("plan_id")
        plan = Plan.objects.get(id=plan_id)

        # Create Razorpay Order
        receipt = f"user{user.id}_plan_{plan.code}_{str(uuid.uuid4())[:8]}"
        order_data = create_order(amount=plan.price, receipt=receipt)
        order_id = order_data["id"]

        # Save in DB
        payment_order = PaymentOrder.objects.create(
            user=user,
            plan=plan,
            order_id=order_id,
            receipt=receipt,
            amount=plan.price,
        )

        return Response({
            "order_id": payment_order.order_id,
            "receipt": payment_order.receipt,
            "amount": payment_order.amount,
            "currency": "INR",
            "razorpay_key": settings.RAZORPAY_KEY_ID,
        })


class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        order_id = request.data.get("order_id")
        payment_id = request.data.get("payment_id")
        signature = request.data.get("signature")

        try:
            verify_payment_signature(order_id, payment_id, signature)
        except SignatureVerificationError:
            return Response({"status": "failed", "error": "Invalid signature"}, status=400)
        except Exception as e:
            return Response({"status": "failed", "error": str(e)}, status=400)

        # Update DB
        order = PaymentOrder.objects.get(order_id=order_id)
        Payment.objects.create(
            order=order,
            payment_id=payment_id,
            status="success",
            amount=order.amount,
        )
        order.status = "paid"
        order.save()

        profile = order.user.profile
        profile.account_plan = order.plan
        profile.plan_expiry_date = date.today() + timedelta(days=order.plan.duration_days)
        profile.save()

        return Response({"status": "success", "message": "Account upgraded"})
