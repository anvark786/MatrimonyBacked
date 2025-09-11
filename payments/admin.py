from django.contrib import admin

from .models import Plan, PaymentOrder, Payment, Refund 
@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "price", "duration_days", "is_active", "created_at")
    search_fields = ("name", "code")
    list_filter = ("is_active",)
