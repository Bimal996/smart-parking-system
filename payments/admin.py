from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("transaction_uuid", "reservation", "method", "amount", "status", "paid_at")
    list_filter = ("method", "status")
    search_fields = ("transaction_uuid", "reservation__reference")
