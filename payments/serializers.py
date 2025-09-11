from rest_framework import serializers
from .models import PaymentOrder, Payment, Plan

class PlanSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()
    class Meta:
        model = Plan
        fields = "__all__"
    def get_features(self, obj):
        if not obj.description:
            return []
        return [feature.strip() for feature in obj.description.split(',')]


class PaymentOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentOrder
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
